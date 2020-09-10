from django.contrib import admin
from .models import Album, Student
from .models import Song
from .models import DepartmentsData, EmployeesData
# Register your models here.

admin.site.register(DepartmentsData)
admin.site.register(EmployeesData)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Student)
