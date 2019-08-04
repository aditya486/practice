from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from pus.admin import EmployeeResource
from .utils import generate_pdf
import io
from django.views.generic import View
import xlsxwriter


# Create your views here.
def list(request):
    emp = Employee.objects.order_by("id").all()
    # print(emp)
    return render(request, 'pus/list.html', {'emp': emp})


def export(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def detail(request, id):
    # print(request.user)
    emp = Employee.objects.get(id=id)
    return render(request, 'pus/detail.html', {'emp': emp})


def pdf_view(request):
    resp = HttpResponse(content_type='application/pdf')
    emp = Employee.objects.all()
    context = {
        'emp': emp
    }
    result = generate_pdf('pus/pdf.html', file_object=resp, context=context)
    return result


def get_simple_table_data():
    # Simulate a more complex table read.
    return [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]


class MyView(View):

    def get(self, request):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Get some data to write to the spreadsheet.
        # data = get_simple_table_data()
        #
        # # Write some test data.
        # for row_num, columns in enumerate(data):
        #     for col_num, cell_data in enumerate(columns):
        #         worksheet.write(row_num, col_num, cell_data)
        # url = 'pus/fun.jpg'
        # image_data = io.BytesIO(urllib2.urlopen(url).read())
        # worksheet.set_column('C:C', 20)
        # worksheet.set_row(0, 40)
        # worksheet.set_row(1, 100)
        # worksheet.merge_range('C2:C3', 'gdfcngng')
        # worksheet.merge_range(2, 1, 3, 3, 'Merged Cells')
        worksheet.merge_range('B3:D4', 'Merged Cells')
        # worksheet.insert_image('A1', 'pus/static/pus/logo.png', {'x_scale': 0.3, 'y_scale': 0.3})

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'django_simple.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
