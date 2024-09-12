from django.shortcuts import render, redirect
from .forms import ImagesForm
from .models import Image
from RilevaMatricole.functions.Img2Barcode import scanPhoto, scanPhoto_TEST
from django.http import FileResponse
import os
from datetime import datetime


def clearHistory():
    files = os.listdir('media/RilevaMatricole_Images')

    for file in files:
        os.remove('media/RilevaMatricole_Images/'+file)

    Image.objects.all().delete()
    # for i in range(len(images)+1000):
    #     try:
    #         Image.objects.get(id=i).delete()
    #     except:
    #         A = 2


def download_file(file):
    response = FileResponse(open(file, 'rb'), as_attachment=True, filename=file)
    return response


def download_excel(request):
    folder_path = r"media\RilevaMatricole_Images"
    files = os.listdir(folder_path)

    start = datetime.now()
    file_name = scanPhoto_TEST(folder_path, files)
    end = datetime.now()

    print("TEMPO DI SCANSIONE: "+str(end-start))
    clearHistory()

    response = FileResponse(open(file_name, 'rb'), as_attachment=True, filename=file_name)

    return response


# Create your views here.
def index(request):

    start = datetime.now()
    images = Image.objects.all()
    context = {'images': images}

    end = datetime.now()

    delta = end - start

    return render(request, "index.html", context)


def fileupload(request):

    clearHistory()
    form = ImagesForm(request.POST, request.FILES)
    if request.method == 'POST':
        images = request.FILES.getlist('pic')

        for image in images:
            image_ins = Image(pic=image, file_name=image.name)
            image_ins.save()
        return redirect('index')

    context = {'form': form}

    return render(request, "upload.html", context)
