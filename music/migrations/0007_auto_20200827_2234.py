# Generated by Django 3.1rc1 on 2020-08-27 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_departments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Departments',
            new_name='DepartmentsData',
        ),
        migrations.AlterModelTable(
            name='departmentsdata',
            table='departments',
        ),
    ]
