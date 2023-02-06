from datetime import datetime

from django.contrib import messages
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy

from .forms import UploadForm
from .models import UploadFile


class PictureCreateView(CreateView):
    """[1]forms.py　class UploadForm(forms.ModelForm)を引数にとる"""
    model = UploadFile
    fields = '__all__'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        from実行前の処理
        fromに表示するタイトル、uploadするフオームクラスを戻り値として返す
        :param context["title"] :フォームに表示するタイトル名
               context["upload_form"] :class UploadForm
               　　　　　　　　　　　　　　　forms.ModelForm
        :return:context タイトルとモデルフォームを格納した辞書型オブジェクト
        """
        context = super().get_context_data(**kwargs)
        context = {
            'title': "☆画像のアップロード☆",
            'upload_form': UploadForm(),
        }
        return context

    def form_valid(self, upload_form):
        """
        投稿されたファイルのファイル名を取得して file_name 属性に格納する
        instance.file_nameは、フォームに入力した文字列＋日付時刻でオーバーライドした
        :param upload_form:　写真をアップロードするフォームクラス
            　　instance:データベースへ保存する前のモデルインスタンスのリスト
               instanceのタイプは、<class 'dl.models.UploadFile'>
        :return:
        """

        instance = upload_form.save(commit=False)
        print(instance, "instance")
        # file_nameをフォームで入力した文字列にする時は、以下のコードは実行しない
        instance.file_name = f'{instance.file_name}_{datetime.today().strftime("%Y%m%d")}'
        instance.save()
        # saveすると、instanse.file_nameに名前が格納された

        messages.success(self.request, f'id:{instance.id} {instance.file_name}のファイルをアップロードしました。')
        print(type(messages), "message")
        return super().form_valid(upload_form)

    def get_success_url(self):
        return self.request.path


class UpdateView(CreateView):
    """[2] upload.html formのテンプレートを活用する"""
    model = UploadFile
    fields = '__all__'
    template_name = 'upload.html'

    def form_valid(self, form):
        """
        投稿されたファイルのファイル名を取得して file_name 属性に格納する
        instance.file_nameは以下の名前でオーバーライド
        アップロードした画像ファイル名＋"html formのテンプレートからupload"
        :param form:　upload.htmlのテンプレートフォーム
            　　instance:データベースへ保存する前のモデルインスタンスのリスト
               instanceのタイプは、<class 'dl.models.UploadFile'>
        :return:
        """
        instance = form.save(commit=False)
        # instance.file_nameをオーバーライドしないと、フォームに入力したファイル名
        instance.file_name = instance.file.name + "html formのテンプレートからupload"
        instance.save()
        # saveすると、instance.file_nameに名前が格納された

        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class PictureList(ListView):
    """画像のid、写真，削除リンクを表示する一覧ページ"""
    model = UploadFile
    template_name = 'list.html'


class PictureDeleteView(DeleteView):
    """画像を削除するページ"""
    model = UploadFile
    template_name = 'delete_file.html'
    success_url = reverse_lazy('pictures:list')

    def delete(self, request, *args, **kwargs):
        """
        Pkを指定しないと削除ができなかったので、self.get_objectの引数にpkを渡した
        """
        self.object = self.get_object(pk=pk)
        success_url = self.get_success_url()
        self.object.delete(pk=pk)
        return reverse_lazy(success_url)
