# Generated by Django 2.1.5 on 2019-08-04 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pus', '0003_employee_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='image',
        ),
    ]
