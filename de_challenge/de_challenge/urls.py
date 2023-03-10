"""de_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from employees.urls import router as employees_router
from employees.urls import report_urlpatterns
from employees.views import create_avro_backup, restore_backup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(employees_router.urls)),
    path('reports/', include(report_urlpatterns)),
    path('backup/<str:table>/', create_avro_backup, name='backup'),
    path('backup_restore/<str:table>/', restore_backup, name='backup'),
]
