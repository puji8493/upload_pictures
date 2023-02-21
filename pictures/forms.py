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

    def is_valid(self):
        print('modelform_isvarid実行')
        return super().is_valid()


class CheckValidationForm(forms.Form):
    """clean処理を用いたフォーム作業 CheckValidationView(FormView)で使用"""

    file = forms.ImageField(label='登録ファイル')
    file_name = forms.CharField(label='ファイル名')

    def clean_file(self):
        """
        ファイル容量が500KBを超えていたらエラーを返す

        :param: file:バリデーションを実行された後に生成される辞書
        　　　　指定されたキーが存在しない場合はNoneを返すself.cleanded_data.get()メソッドにしてみた
        :return:エラーの場合はValidationErrorを返す:
                エラーがない場合はfileオブジェトクを返す
        """

        file = self.cleaned_data.get('file')

        print(self.cleaned_data['file'])  # ULCA0005.JPG
        print(type(self.cleaned_data['file']))  # <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>

        if file and file.size > 500 * 1000:
            raise forms.ValidationError('ファイルサイズは500KB以下にしてください')
        return file

    def clean_file_name(self):
        """
        特定のフィールド属性をクリーニングする
        file_nameが"test"だったら、エラーを返す

        :param: file:バリデーションを実行された後に生成される辞書
        　　　　指定されたキーが存在しない場合はNoneを返すself.cleanded_data.get()メソッドにしてみた
        :return:エラーの場合はValidationErrorを返す:
                エラーがない場合はfileオブジェトクを返す
        """

        file_name = self.cleaned_data['file_name']
        # cleaned_data = super().clean()
        # file_name = cleaned_data['file_name']
        print(file_name, "check_clean_file", sep="☆")
        if file_name == "test":
            raise forms.ValidationError('ファイル名にtestという名前は使用できません')
        return file_name


class CheckValidationModelForm(forms.ModelForm):
    """clean処理を用いたフォーム作業 ModelForm"""
    class Meta:
        model = UploadFile
        fields = '__all__'

    def clean_file_name(self):
        file_name = self.cleaned_data['file_name']
        print("formのcleanソメッドでfile_name検索：", file_name)
        if 'test' in file_name:
            raise forms.ValidationError(f'{file_name}はだめてす')
        return file_name


class EditByFormsForm(forms.Form):
    """画像を編集(差替）するフォーム"""

    file = forms.ImageField(label='編集ファイル')
    file_name = forms.CharField(label='編集ファイル名')

    def is_valid(self):
        print("is_valid()が実行されました")
        return super().is_valid()

    def get_initial(self):
        instance = UploadFile.objects.get(pk=self.kwargs['pk'])
        return {"file": instance.file, "file_name": instance.file_name}

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > 500 * 1000:
            raise forms.ValidationError('ファイルサイズは500KB以下にしてください')
        return file


class DeleteForm(forms.Form):
    """画像を削除するフォーム"""

    id = forms.IntegerField(label='削除する画像のID', widget=forms.HiddenInput)
