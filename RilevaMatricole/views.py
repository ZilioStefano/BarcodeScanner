from django.shortcuts import render, redirect
from .forms import ImagesForm
from .models import Image
from RilevaMatricole.functions.Img2Barcode import scanPhoto
from django.http import FileResponse
import os


def clearHistory():
    files = os.listdir('media/RilevaMatricole_Images')

    for file in files:
        os.remove('media/RilevaMatricole_Images/'+file)

    images = Image.objects.all()
    for i in range(len(images)+1000):
        try:
            Image.objects.get(id=i).delete()
        except:
            A = 2


def download_file(file):
    response = FileResponse(open(file, 'rb'), as_attachment=True, filename=file)
    return response


def download_excel(request):
    folder_path = r"media\RilevaMatricole_Images"
    files = os.listdir(folder_path)
    file_name = scanPhoto(folder_path, files)
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
    form = ImagesForm(request.POST, request.FILES)
    if request.method == 'POST':
        images = request.FILES.getlist('pic')

        for image in images:
            image_ins = Image(pic=image)
            image_ins.save()
        return redirect('index')

    context = {'form': form}
    return render(request, "upload.html", context)
