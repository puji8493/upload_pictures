from django import forms
from django.core import validators

from .models import UploadFile


class UploadForm(forms.ModelForm):
    """画像をアップロードするフォーム"""

    class Meta:
        model = UploadFile
        # fields = '__all__'
        fields = ('file', 'file_name')

        file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'file-name'}))


class EditForm(forms.ModelForm):
    """画像を編集(差替）するフォーム"""

    class Meta:
        model = UploadFile
        fields = '__all__'


# class CreateForms2(forms.ModelForm):
#     class Meta:
#         model = UploadFile
#         fields = '__all__'
#
#     def clean_file_name(self):
#         file_name = self.cleaned_data['file_name']
#         print("name検索", file_name)
#         if 'book' in file_name:
#             raise forms.ValidationError(f'{file_name}はだめてす')
#         return file_name


class CheckValidationForm(forms.Form):
    """clean処理を用いたフォーム作業"""

    file = forms.ImageField(label='登録ファイル')
    file_name = forms.CharField(label='ファイル名')

    def clean_file_name(self):
        cleand_data = super().clean()
        file_name = cleand_data['file_name']
        print(file_name, "check_clean_file", sep="☆")
        if file_name == "test":
            raise forms.ValidationError('ファイル名にtestという名前は使用できません')
        return file_name
