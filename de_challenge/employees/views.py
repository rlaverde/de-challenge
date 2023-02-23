import logging
import os

from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection, transaction
import pandas as pd
import fastavro
from datetime import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from .models import Employee, Job, Department
from .serializers import EmployeeSerializer, DepartmentSerializer, JobSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class JobViewSet(viewsets.ModelViewSet):
    """"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def hired_by_quarter(request):
    """
    Return a list of all employees hired by quarter.
    """

    query = """
SELECT department,
       job,
       SUM(quarter=0) AS Q1,
       SUM(quarter=1) AS Q2,
       SUM(quarter=2) AS Q3,
       SUM(quarter=3) AS Q4
FROM
  (SELECT *, CAST(strftime('%m', datetime) AS INTEGER) % 4 AS quarter
   FROM employees_employee
   WHERE strftime('%Y', datetime) = '2021') e
JOIN employees_job j ON e.job_id = j.id
JOIN employees_department d ON e.department_id = d.id
GROUP BY department, job
ORDER BY department, job ;
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return JsonResponse(dictfetchall(cursor), safe=False)


def departmet_most_hires(request):
    """
    Return a list of departments that hired more than the mean.
    """

    query = """
SELECT department_id, department, COUNT(*) as num_hires
FROM employees_employee e
JOIN employees_department d ON e.department_id = d.id
WHERE strftime('%Y', datetime) = '2021'
GROUP BY department_id
HAVING COUNT(*) > (SELECT AVG(num_hires) FROM (SELECT department_id, COUNT(*) as num_hires FROM employees_employee WHERE strftime('%Y', datetime) = '2021' GROUP BY department_id) as temp)
ORDER BY num_hires DESC;
"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        return JsonResponse(dictfetchall(cursor), safe=False)


def generate_avro_schema(Model):
    # Get the metadata of the Django model
    meta = Model._meta

    # Define the Avro schema fields
    fields = []
    for field in meta.fields:
        field_type = field.get_internal_type()
        field_name = field.name
        if field_type == 'CharField':
            avro_type = 'string'
        elif field_type in ('IntegerField', 'PositiveIntegerField'):
            avro_type = 'int'
        elif field_type == 'DateTimeField':
            avro_type = 'string'
            avro_type = {"type": "int", "logicalType": "date"}
        elif field_type == 'ForeignKey':
            field_name = field.name + "_id"
            avro_type = 'int'
        else:
            # handle other field types here
            pass
            #avro_type = ""
        fields.append({'name': field_name, 'type': avro_type})

    # Define the Avro schema
    schema = {
        'namespace': meta.app_label,
        'name': meta.object_name,
        'type': 'record',
        'fields': fields
    }

    return schema


TABLE_TO_MODEL = {"employee": Employee, "department": Department, "job": Job}


def create_avro_backup(request, table):

    model = TABLE_TO_MODEL[table]

    query = str(model.objects.all().query)
    df = pd.read_sql_query(query, connection)
    records = df.to_dict(orient='records')

    schema = generate_avro_schema(model)

    avro_data = {'schema': schema, 'records': records}

    # Write to Avro file
    with open(f'{table}_{datetime.now().isoformat()}.avro', 'wb') as avro_file:
        fastavro.writer(avro_file, schema, avro_data['records'])

    return JsonResponse({"status": "OK", "records_backup": len(records)})


def get_latest_backup(table):

    # Get a list of all files in the current directory
    files = os.listdir()

    # Create a list of tuples containing the filename and the timestamp as a datetime object
    timestamps = []
    for file in files:
        if file.startswith(table) and file.endswith(".avro"):
            print(file)
            timestamp = file.split(".")[0].rsplit("_", 1)[1]
            timestamps.append([file, datetime.fromisoformat(timestamp)])

    # Sort the list of timestamps by the timestamp (newest first)
    timestamps.sort(key=lambda x: x[1], reverse=True)

    # Get the filename of the latest file
    latest_file = timestamps[0][0]

    return latest_file


def restore_backup(request, table):
    model = TABLE_TO_MODEL[table]
    backup_file = get_latest_backup(table)

    with open(backup_file, 'rb') as f:
        reader = fastavro.reader(f)
        for row in reader:
            try:
                if model == Employee:
                    row["department"] = Department.objects.get(
                        pk=row.pop("department_id"))
                    row["job"] = Job.objects.get(pk=row.pop("job_id"))
                with transaction.atomic():
                    model.objects.create(**row)
            except IntegrityError as e:
                logging.error('Error inserting: %s', row["id"])

    return JsonResponse({"status": "OK"})
