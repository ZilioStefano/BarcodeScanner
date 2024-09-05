from django.urls import path
from . import views

urlpatterns = [

    path('upload', views.index, name='index'),
    path('', views.fileupload, name="File_Uploads"),
    path('download', views.download_excel, name="downloadexcel"),

]