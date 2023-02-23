# Code Challenge Data Enginner

# Install

Create environment and install requirements:

using pipenv:

```
$ pipenv install
```

using pip:

```
$ pip install requirements.txt
```

# Running

Run migrations, this will aso load initial data:

```
$ python manage.py migrate
```

Start django service:

```
$ python manage.py runserver
```

# API endpoints

## REST Endpoints

For adding and modifing data

jobs: "http://127.0.0.1:8000/api/jobs/",
departments: "http://127.0.0.1:8000/api/departments/",
employees: "http://127.0.0.1:8000/api/employees/"

# Reports

Employees hired by Department and Job by Quarter

http://127.0.0.1:8000/reports/hired_by_quarter

Department with most hires:

http://127.0.0.1:8000/reports/departmet_most_hires

## Backup

Creating avro backup:

http://127.0.0.1:8000/backup/employee/
http://127.0.0.1:8000/backup/department/
http://127.0.0.1:8000/backup/job/

Restoring latest avro backup:

http://127.0.0.1:8000/backup_restore/employee/
http://127.0.0.1:8000/backup_restore/department/
http://127.0.0.1:8000/backup_restore/job/
