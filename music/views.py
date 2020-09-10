from django.db.models import Q
from django.views import generic
from .models import Album, Student, DepartmentsData, EmployeesData, Absencedata, Attachmentsdata
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
#from pagination.models import Student
from django.core.paginator import Paginator
import csv
from io import BytesIO
from xhtml2pdf import pisa
from django.template import Context
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
import string
from django.utils.safestring import mark_safe
from datetime import date
from django.db import transaction
import json


def deleteattachment(request, attachment_id):
    absenceid = request.session.get("absenceid")
    print("attachment_id::" + str(attachment_id))
    print("absenceid::" + str(absenceid))
    #print("absenceid in upload ::" + str(absenceid))
    attachment_type = request.session.get("attachment_type")
    print("attachment_type::" + attachment_type)
    #del_attachments = Attachmentsdata.objects.filter(pk=attachment_id)
    #del_attachments = get_object_or_404(Attachmentsdata, pk=attachment_id)
    del_attachments = Attachmentsdata.objects.get(pk=int(request.POST['id']))
    del_attachments.is_deleted = 'Y'
    del_attachments.delete()
    #for z in del_attachments:
    print("Attahcment from table ::" + str(del_attachments.id))
    #del_attachments.save()
    #all_attachments = Attachmentsdata.objects.filter(
        #transaction_id=absenceid, attachment_type=attachment_type, is_deleted="N")
    #return HttpResponseRedirect('http://127.0.0.1:8000/music/upload/', {'all_attachments': all_attachments})
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')
    #return HttpResponseRedirect('/music/', {'all_employees': all_employees})

    #return upload(request)


def createleave(request):
    absencedata = Absencedata()
    if request.method == 'POST':
        if request.POST.get('apply') or request.POST.get('attach'):
            if 'apply' in request.POST:
                print("Inside create btn")
                print("request.POST.get('leavetype')::" + str(request.POST.get('leavetype')))
                print("request.POST.get('startdate')::" + request.POST.get('leavetype'))
                print("request.POST.get('enddate')::" + request.POST.get('enddate'))
                recid = insertdata(request, request.POST.get('leavetype'), request.POST.get('startdate'), request.POST.get('enddate'))
                print("Generated apply id is ::" + str(recid))
            if 'attach' in request.POST:
                print("Inside attach btn")
                recid = insertdata(request, request.POST.get('leavetype'), request.POST.get('startdate'), request.POST.get('enddate'))
                print("Generated id attach ::" + str(recid))
                request.session["absenceid"] = str(recid)
                request.session["attachment_type"] = 'Absence'
            #print("Inside button press attach::" + request.POST.get('attach'))
            #return render(request, 'music/upload.html')
            return HttpResponseRedirect('/music/upload/', )
    return render(request, 'music/createleave.html')


def insertdata(request, pleave_type, pstart_date, pend_date):
    absencedata = Absencedata()
    #print("pleave_type::" + str(pleave_type))
    #print("pstart_date::" + str(pstart_date))
    #print("pend_date::" + str(pend_date))
    #print("new Date year::" + pstart_date[6:10])
    #print("new Date month::" + pstart_date[3:5])
    #print("new Date day::" + pstart_date[0:2])


    absencedata.leave_type = pleave_type
    absencedata.start_date = pstart_date[6:10] + '-' + pstart_date[3:5] + '-' + pstart_date[0:2]
    absencedata.end_date = pend_date[6:10] + '-' + pend_date[3:5] + '-' + pend_date[0:2]
    absencedata.save()
    print("New generated id is ::" + str(absencedata.pk))
    return absencedata.pk


def gotoeditpage(request, employeeid):
    print("from edit page employee id is ::" + str(employeeid))
    employees = get_object_or_404(EmployeesData, pk=employeeid)
    employees_sel = EmployeesData.objects.get(pk=employeeid)
    print("employee id fetched::" + str(employees_sel.id))
    #employees = get_object_or_404(EmployeesData, pk=employeeid)
    all_departments = DepartmentsData.objects.all()
    one_department = DepartmentsData.objects.filter(id=employees.department_id)
    transaction.set_autocommit(False)
    is_changed = False
    if request.method == 'POST':
        print("1")
        if employees_sel.first_name != request.POST.get('firstname'):
            employees_sel.first_name = request.POST.get('firstname')
            is_changed = True
            print("2")
        if employees_sel.middle_name != request.POST.get('middlename'):
            employees_sel.middle_name = request.POST.get('middlename')
            is_changed = True
            print("3")
        if employees_sel.last_name != request.POST.get('lastname'):
            employees_sel.last_name = request.POST.get('lastname')
            is_changed = True
            print("4")
        if employees_sel.department_id != request.POST.get('departmentname'):
            employees_sel.department_id = request.POST.get('departmentname')
            is_changed = True
            print("5")
        if employees_sel.email_id != request.POST.get('emailid'):
            employees_sel.email_id = request.POST.get('emailid')
            is_changed = True
            print("6")
        if employees_sel.date_of_birth != request.POST.get('dob'):
            employees_sel.date_of_birth = request.POST.get('dob')
            is_changed = True
            print("7")

        print("Boolean value::" + str(is_changed))
        if is_changed:
            employees_sel.save()
            transaction.commit()

        all_employees = EmployeesData.objects.all()
        return HttpResponseRedirect('/music/', {'all_employees': all_employees})

    for result in one_department:
        print("Department name and id is ::" + str(result.id) + "::Name is:: " + result.department_name)
    # return render(request, 'music/detail.html', {'albums': albums})
    return render(request, 'music/editemployee.html', {'employees': employees, 'all_departments': all_departments,
                                                       'one_department': one_department})


def gotodeletepage(request, employeeid):

    print("from delete page employee id is ::" + str(employeeid))
    employees = get_object_or_404(EmployeesData, pk=employeeid)

    # return render(request, 'music/detail.html', {'albums': albums})
    return render(request, 'music/deleteemployee.html', {'employees': employees})


def deleteemployee(request, employeeid):
    transaction.set_autocommit(False)
    print("from delete view employee id is ::" + str(employeeid))
    #return HttpResponse("<h2>Details for Album id::" + str(album_id) + "</h2>")
    #albums = get_object_or_404(Album, pk=album_id)
    employee = get_object_or_404(EmployeesData, pk=employeeid)
    all_employees = EmployeesData.objects.all()
    if request.method == 'POST':
        print("Inside delete post 1")
        #saverecord = EmployeesData(employees)
        print("Inside delete post val::" + str(employee.id))
        employee1 = get_object_or_404(EmployeesData, pk=employeeid)
        employee1.delete()
        transaction.commit()
        #employee1.save()
        return HttpResponseRedirect('/music/', {'all_employees': all_employees})
    else:
        return render(request, 'music/deleteemployee.html', {'employees': employee})


def index(request):
    all_albums = Album.objects.all()
    all_departments = DepartmentsData.objects.all()
    #dict = {'name': 'vikas'}
    all_employees = EmployeesData.objects.all()
    name = "j"
    #query = "select id,first_name from employees where id=1 and middle_name='chandra' " \
            #"and last_name like '%%" + name + "%%'"
    #all_employees = EmployeesData.objects.raw(query)
    #request.session["name"] = "vikas session variable"
    #del request.session['name']
    #equest.session["name"] = "vikas session variable new"
    #context['uploaded_file_url'] = 'vikas'
    #half = all_employees.count() / 2
    #return {'sports_1': sports[0:half], 'sports_2': sports[half:]}
    #context = {'employees_1': all_employees[0:half], 'employees_2': all_employees[half:]}
    context = {'all_employees': all_employees, 'dict': dict}
    return render(request, 'music/index.html', context)
    if request.method == 'POST':
        if request.POST.get("createemp"):
            context = {'all_departments': all_departments}
            return render(request, 'music/createemprecord.html', context)

    else:
        #template = loader.get_template('music/index.html')
        context = {'all_albums': all_albums}
        return render(request, 'music/index.html', context)
    #return HttpResponse(template.render(context, request))


def gotoempcreate(request):
    all_departments = DepartmentsData.objects.all();
    context = {'all_departments': all_departments}
    messages.success(request, '')
    return render(request, 'music/createemprecord.html', context)


def createemprecord(request):
    print("Inside createemprecord")
    #all_albums = Album.objects.all()
    print("Inside createemprecord 1" + request.method + "::Message length::" + str(len(str(messages))))
    if request.method == 'POST':# and len(str(messages)) == 0:
        print("Inside createemprecord 2")
        if 'createbtn' in request.POST: #request.POST.get("createbtn"):
            print("Inside create")
            saverecord = EmployeesData()
            print("Inside create 1")
            print("Inside createemprecord department id::" + str(request.POST.get('departmentname')))
            saverecord.department_id = request.POST.get('departmentname')
            print("Inside create 2")
            saverecord.first_name = request.POST.get('firstname')
            print("Inside create 3")
            saverecord.middle_name = request.POST.get('middlename')
            print("Inside create 4")
            saverecord.last_name = request.POST.get('lastname')
            print("Inside create 5")
            saverecord.email_id = request.POST.get('emailid')
            print("Inside create 6 dob::-" + str(request.POST.get('dob')))
            saverecord.date_of_birth = request.POST.get('dob')
            print("Inside create 7 date is ::" + str(date.today()))
            creation_date = date.today()
            print("Inside create 8")
            last_update_date = date.today()
            print("Inside create 9")
            created_by = 2
            print("Inside create 10")
            last_updated_by = 2
            print("Inside create 11")
            image_url = "1.JPG"
            print("Inside create 11.5")
            saverecord.save()
            #transaction.rollback()
            print("New rcord id is::" + str(saverecord.pk))
            print("Inside create 12")
            messages.success(request, 'Record Saved Successfully')
            print("Inside create 13")
            #context = {'all_albums': all_albums}
            context = {}
            print("Inside create 14")
            return render(request, 'music/createemprecord.html', context)
        if 'cancelbtn' in request.POST: #request.POST.get("cancelbtn"):
            #messages.success(request, 'Record Saved Successfully')
            #context = {'all_albums': all_albums}
            all_employees = EmployeesData.objects.all()

            context = {'all_employees': all_employees, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'music/index.html', context)
    else:
        #context = {'all_albums': all_albums}
        context = {}
        return render(request, 'music/index.html', context)


def detail(request, album_id):
    #return HttpResponse("<h2>Details for Album id::" + str(album_id) + "</h2>")
    #albums = get_object_or_404(Album, pk=album_id)
    employee = get_object_or_404(EmployeesData, pk=album_id)
    #return render(request, 'music/detail.html', {'albums': albums})
    return render(request, 'music/detail.html', {'employee': employee})


def favorite(request, album_id):
    #logger.warning("album_id::"+album_id)
    print("album_id::"+ str(album_id))
    albums = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = albums.song_set.get(pk=request.POST['song'])
        #logger.warning("after selected_song::" + album_id)
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'albums': albums,
            'error_message': "You did not select a valid song",
            })
    else:
        #logger.warning("Inside else::" + album_id)
        selected_song.is_favorite = True
        #logger.warning("Inside else after set::" + album_id)
        selected_song.save()
        #logger.warning("Inside else after save::" + album_id)
        #return render(request, 'music/detail.html', {'albums': albums})
        return render(request, 'music/detail.html', {'albums': albums})


def search(request):
    results = Student.objects.all()
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    context = {'sr': results}
    return render(request, 'music/search.html', context)


def createdepartment(request):
    context = {}
    if request.method == 'POST':
        departmentname = request.POST['department_name']



def lovfromdb(request):
    results = DepartmentsData.objects.all()
    context = {'results': results}
    return render(request, 'music/dynamicLov.html', context)


def upload(request):
    context = {}

    if request.method == 'POST':
        print("Inside post of upload")
        if 'loadfile' in request.POST:
            print("Inside post of loafile button")
            absenceid = request.session.get("absenceid")
            print("absenceid in upload ::" + str(absenceid))
            attachment_type = request.session.get("attachment_type")
            print("attachment_type in upload ::" + attachment_type)
            upload_file = request.FILES['document']
            print("upload_file name" + upload_file.name)
            print("upload_file size" + str(upload_file.size))
            fs = FileSystemStorage()
            #file_name = upload_file.name

            file_name_full = upload_file.name
            print("Uploaded file name full::" + file_name_full)

            dotplace = file_name_full.find('.')

            file_name = file_name_full[0:dotplace]
            file_extension = file_name_full[dotplace+1:]

            print("Uploaded file name for save ::" + file_name)
            print("Uploaded file name for save file_extension::" + file_extension)

            print("Uploaded file name dotplace::" + str(dotplace))
            print("File name is ::" + file_name_full[0:dotplace])
            print("File extension is ::" + file_name_full[dotplace+1:])
            name = fs.save(file_name + '-' + absenceid + '.' + file_extension, upload_file)
            print("Saved File is :: " + file_name)
            url = fs.url(name)
            print("First url " + url)
            #new_str =  url
            finalUrl = url.replace("media", "music/media")
            context['url'] = finalUrl
            print("after file save")

            attachmentsdata = Attachmentsdata()
            attachmentsdata.transaction_id = absenceid
            attachmentsdata.attachment_type = attachment_type
            attachmentsdata.file_name = file_name + '-' + absenceid
            attachmentsdata.file_extension = file_extension
            attachmentsdata.is_deleted = 'N'
            attachmentsdata.save()
            all_attachments = Attachmentsdata.objects.filter(transaction_id=absenceid, attachment_type=attachment_type)
            return render(request, 'music/upload.html', {'all_attachments': all_attachments})

    absenceid = request.session.get("absenceid")
    print("absenceid in upload ::" + str(absenceid))
    attachment_type = request.session.get("attachment_type")
    all_attachments = Attachmentsdata.objects.filter(
        transaction_id= absenceid, attachment_type=attachment_type, is_deleted="N")
    return render(request, 'music/upload.html', {'all_attachments': all_attachments})


def exportdata(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'email', 'city', 'marks'])
    results = Student.objects.all().values_list('name', 'email', 'city', 'marks')
    #users = User.objects.all().valresultsues_list('username', 'first_name', 'last_name', 'email')
    for result in results:
        writer.writerow(result)

    return response


def generate_PDF(request):
    results = Student.objects.all().values_list('name', 'email', 'city', 'marks')
    #results = Student.objects.filter(Q(name__icontains="vikas"))
    context = {'sr': results}
    template = get_template('music/search.html')
    #html = template.render(Context(data))
    html = template.render(context)

    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')
    """
    if request.method == 'POST':
        if request.POST.get("searchbtn"):
            print("Inside search btn")
            srch = request.POST['search']
            match = Student.objects.filter(Q(name__icontains=srch) |
                                           Q(city__icontains=srch))
            print("Inside searchbtn btn count is ::" + str(match))
            context = {'sr': match}
            return render(request, 'music/search.html', context)
        if request.POST.get("resetbtn"):
            print("Inside reset btn")
            srch = "Rajesh"
            match = Student.objects.all()
            print("Inside reset btn count is ::" + str(match))
            context = {'sr': match}
            return render(request, 'music/search.html', context)
    return render(request, 'music/search.html')
    """
