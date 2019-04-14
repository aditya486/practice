from django.contrib import admin
from .models import Employee
from import_export import resources
# Register your models here.

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
admin.site.register(Employee)
