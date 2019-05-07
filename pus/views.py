from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from pus.admin import EmployeeResource
# from django_xhtml2pdf.utils import generate_pdf
import xhtml2pdf.pisa as pisa
from io import StringIO
from django.template.loader import get_template
from django.conf import settings
from django.conf.urls.static import static
import os
from .utils import generate_pdf


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

from django.http import HttpResponse


# def pdf_view(request):
#     resp = HttpResponse(content_type='application/pdf')
    # emp = Employee.objects.all()
    # context = {
    #     'emp': emp
    # }
#     result = generate_pdf('pdf.html', file_object=resp, context=context)
#     return result
def test_view(request):
    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="report.pdf"'

    emp = Employee.objects.all()
    context = {
        'emp': emp
    }
    result = generate_pdf('pus/pdf.html', file_object=resp, context=context)
    return result
