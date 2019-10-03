from django.db import models

# Create your models here.
class UploadFileModel(models.Model):
    title = models.TextField(default="")
    files = models.FileField(null=False, upload_to="%Y-%m-%d")

