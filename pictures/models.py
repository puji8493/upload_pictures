from django.conf import settings
from django.db import models

class UploadFile(models.Model):
    """ファイルとファイルネームのモデル"""

    file = models.ImageField(upload_to='media/images/')
    file_name = models.CharField(max_length=100, verbose_name='ダウンロード時に使うファイル名')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name

class Comment(models.Model):
    """コメントモデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='コメント')
    target = models.ForeignKey(UploadFile, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

