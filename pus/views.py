from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from pus.admin import EmployeeResource

# Create your views here.
def list(request):
    emp = Employee.objects.order_by("id").all()
    # print(emp)
    return render(request, 'pus/list.html',{'emp':emp})


def export(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

def detail(request,id):
    # print(request.user)
    emp = Employee.objects.get(id=id)
    print(emp)
    return render(request, 'pus/detail.html', {'emp': emp})
