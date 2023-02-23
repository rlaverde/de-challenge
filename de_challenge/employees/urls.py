from django.urls import include, path
from rest_framework import routers
from .views import JobViewSet, DepartmentViewSet, EmployeeViewSet, hired_by_quarter, departmet_most_hires

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)

report_urlpatterns = [
    path('hired_by_quarter/', hired_by_quarter),
    path('most_hires/', departmet_most_hires),
]
