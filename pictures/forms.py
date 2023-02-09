from django import forms

from .models import UploadFile


class UploadForm(forms.ModelForm):
    """画像をアップロードするフォーム"""

    class Meta:
        model = UploadFile
        fields = '__all__'


class EditForm(forms.ModelForm):
    """画像を編集(差替）するフォーム"""

    class Meta:
        model = UploadFile
        fields = '__all__'
