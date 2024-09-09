from django.db import models


class Image(models.Model):
    name = 'RilevaMatricole_Images'
    pic = models.FileField(upload_to=name)
    file_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.file_name}"
