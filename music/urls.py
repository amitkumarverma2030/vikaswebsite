from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.index, name='index'),
    # /music/712
    path('<int:album_id>/', views.detail, name='detail'),
    # /music/712/favorite/
    path('<int:album_id>/favorite/', views.favorite, name='favorite'),
    path('search/', views.search, name='search'),
    path('exportdata/', views.exportdata, name='exportdata'),
    path('generate_PDF/', views.generate_PDF, name='generate_PDF'),
    path('upload/', views.upload, name='upload'),
    path('lovfromdb/', views.lovfromdb, name='lovfromdb'),
    path('gotoempcreate/', views.gotoempcreate, name='gotoempcreate'),
    path('createemprecord/', views.createemprecord, name='createemprecord'),
    path('<int:employeeid>/gotodeletepage/', views.gotodeletepage, name='gotodeletepage'),
    path('<int:employeeid>/deleteemployee/', views.deleteemployee, name='deleteemployee'),
    path('<int:employeeid>/gotoeditpage/', views.gotoeditpage, name='gotoeditpage'),
    path('createleave/', views.createleave, name='createleave'),
    path('<int:attachment_id>/deleteattachment/', views.deleteattachment, name='deleteattachment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
