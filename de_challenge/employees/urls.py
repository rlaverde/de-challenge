from django.urls import include, path
from rest_framework import routers
from .views import JobViewSet, DepartmentViewSet, EmployeeViewSet

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
