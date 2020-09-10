from django.db import models
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your models here.


class DepartmentsData(models.Model):
    department_name = models.CharField(max_length=100)
    #id = models.IntegerField()

    class Meta:
        db_table = "departments"

    def __str__(self):
        return self.department_name


class EmployeesData(models.Model):
    department_id = models.IntegerField(blank=True)
    first_name = models.CharField(max_length=100, default='a')
    middle_name = models.CharField(max_length=100, default='a')
    last_name = models.CharField(max_length=100, default='a')
    email_id = models.CharField(max_length=100, default='a')
    date_of_birth = models.DateField(auto_now=False, blank=True)
    creation_date = models.DateField(auto_now=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    created_by = models.IntegerField(default=1)
    last_updated_by = models.IntegerField(default=1)
    image_url = models.CharField(max_length=100, default='1.JPG')

    #id = models.IntegerField()

    class Meta:
        db_table = "employees"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Absencedata(models.Model):
    leave_type = models.IntegerField(blank=True)
    start_date = models.DateField(auto_now=False, blank=True)
    end_date = models.DateField(auto_now=False, blank=True)

    class Meta:
        db_table = "person_absence_details"

    def __str__(self):
        return self.leave_type + " " + self.start_date + " " + self.end_date


class Attachmentsdata(models.Model):
    transaction_id = models.IntegerField(blank=True)
    attachment_type = models.CharField(max_length=100, default='a')
    file_name = models.CharField(max_length=100, default='a')
    file_extension = models.CharField(max_length=100, default='a')
    is_deleted = models.CharField(max_length=100, default='a')

    class Meta:
        db_table = "transaction_attachment_details"

    def __str__(self):
        return self.transaction_id + " " + self.attachment_type + " " + self.file_name


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    album_logo = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + " "+self.artist


class Song(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    file_type = models.CharField(max_length=250)
    song_title = models.CharField(max_length=500)
    is_favorite = models.BooleanField(default=False)
    song_fav_url = models.CharField(max_length=500, default="http:/i.imgur.com/b9b13Rd.png")

    def __str__(self):
        return self.song_title


class Student(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    marks = models.CharField(max_length=500)

    def __str__(self):
        return self.name
