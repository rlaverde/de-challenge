from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection

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
