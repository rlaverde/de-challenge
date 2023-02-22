from .models import Employee, Job, Department
from rest_framework import viewsets
from rest_framework import permissions
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
