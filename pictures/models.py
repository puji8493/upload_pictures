from django.db import models

class UploadFile(models.Model):
    file = models.ImageField(upload_to='media/images/')
    file_name = models.CharField(max_length=100, verbose_name='ダウンロード時に使うファイル名')

    def __str__(self):
        return self.file_name
