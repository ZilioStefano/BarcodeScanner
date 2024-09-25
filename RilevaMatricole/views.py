from django.shortcuts import render, redirect
from .forms import ImagesForm, MethodForm
from .models import Image
from RilevaMatricole.functions.Img2Barcode import scan
from django.http import FileResponse
import os
from datetime import datetime
import pandas as pd


def clearHistory():
    files = os.listdir('media/RilevaMatricole_Images')

    for file in files:
        os.remove('media/RilevaMatricole_Images/'+file)

    Image.objects.all().delete()


def download_file(file):
    response = FileResponse(open(file, 'rb'), as_attachment=True, filename=file)
    return response


def download_excel(request):

    method = pd.read_csv("method.csv")
    method = method["method"]

    folder_path = r"media\RilevaMatricole_Images"
    files = os.listdir(folder_path)

    start = datetime.now()
    file_name = scan(method, folder_path, files)
    end = datetime.now()

    print("TEMPO DI SCANSIONE: "+str(end-start))
    clearHistory()

    response = FileResponse(open(file_name, 'rb'), as_attachment=True, filename=file_name)

    return response


# Create your views here.
def index(request):

    images = Image.objects.all()
    context = {'images': images}

    return render(request, "index.html", context)


def fileupload(request):

    clearHistory()
    upload_form = ImagesForm(request.POST, request.FILES)

    if request.method == 'POST':
        images = request.FILES.getlist('pic')
        method = pd.DataFrame({"method": request.POST['method']}, index=[0])
        method.to_csv("method.csv", index=False)

        for image in images:
            image_ins = Image(pic=image, file_name=image.name)
            image_ins.save()
        return redirect('index')

    method_form = MethodForm(request.POST, request.FILES)

    context = {'upload_form': upload_form, 'method_form': method_form}

    return render(request, "upload.html", context)
