from django.db import models
from datetime import datetime


class Image(models.Model):

    start = datetime.now()
    print("Sono in form")
    name = 'RilevaMatricole_Images'
    pic = models.FileField(upload_to=name)
    file_name = models.CharField(max_length=100, null=True)

    stop = datetime.now()

    delta = stop - start

    B = 3

    def __str__(self):
        return f"{self.file_name}"
