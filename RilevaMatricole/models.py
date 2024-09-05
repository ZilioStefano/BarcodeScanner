from django.db import models


class Image(models.Model):
    name = 'RilevaMatricole_Images'
    pic = models.FileField(upload_to=name)
