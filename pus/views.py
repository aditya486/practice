from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from pus.admin import EmployeeResource
# from django_xhtml2pdf.utils import generate_pdf
import xhtml2pdf.pisa as pisa
from io import StringIO
from django.template.loader import get_template


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
#     emp = Employee.objects.all()
#     context = {
#         'emp': emp
#     }
#     result = generate_pdf('pdf.html', file_object=resp, context=context)
#     return result
def pdf_view(request):
    emp = Employee.objects.all()
    template_path = 'pus/pdf.html'
    context = {'pagesize': 'A4',
               'emp': emp,
               }    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
        
def link_callback(uri, rel):
    path = os.path.join(conf_settings.MEDIA_ROOT,
                        uri.replace(conf_settings.MEDIA_URL, ""))
    return path
