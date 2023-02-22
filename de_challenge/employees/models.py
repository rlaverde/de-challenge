from django.db import models

# Create your models here.


class Department(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.department


class Job(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    job = models.CharField(max_length=200)

    def __str__(self):
        return self.job


class Employee(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField('hire datetime')

    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    job = models.ForeignKey(Job, on_delete=models.PROTECT)
