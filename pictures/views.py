from datetime import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy

from .forms import UploadForm, EditForm
from .models import UploadFile


class MyFormValidMixin:
    """Mixinクラス　新規登録、編集時のファイルの処理を共通化したメソッドを定義"""
    def my_form_valid(self, form):
        """投稿されたファイル名を入力したファイル名＋日付にする"""

        print("mixin呼び出されました","●")
        instance = form.save(commit=False)
        if instance.file:
            instance.file_name = f'{instance.file_name}_{datetime.today().strftime("%Y%m%d")}'
        print(instance.file_name,"instance.file_name",sep=":")
        instance.save()
        return super().form_valid(form)


class PictureCreateView(MyFormValidMixin, SuccessMessageMixin, CreateView):
    """[1]forms.py　class UploadForm(forms.ModelForm)を引数にとる"""

    model = UploadFile
    fields = '__all__'
    template_name = 'top.html'

    def get_context_data(self, **kwargs):
        """
        fromに表示するタイトル、uploadするフオームクラスを戻り値として返す
        :param context["title"] :フォームに表示するタイトル名
               context["upload_form"] :class UploadForm
        :return:context タイトルとモデルフォームを格納した辞書型オブジェクト
        """

        context = super().get_context_data(**kwargs)
        context = {
            'title': "☆画像のアップロード☆",
            'upload_form': UploadForm(),
        }
        return context

    def get_success_message(self, cleaned_data):
        """
        更新時のメッセージを表示
        :param cleaned_data:'file(InMemoryUploadedFile)'と'file_name'の辞書
        {'file': <InMemoryUploadedFile: IMG_2174.JPG (image/jpeg)>, 'file_name': 'rapping'}
        :return:カスタマイズした成功時のメッセージ(新規登録）
        """

        print(cleaned_data, "☆cleand_data")
        return f'ファイルを{cleaned_data.get("file_name")}で新規登録しました☆'

    def form_valid(self, form):
        """Mixinクラス MyFormValidMixinのform_validを呼び出す"""

        return self.my_form_valid(form)

    def get_success_url(self):
        """成功時にリダイレクトするURL"""

        return self.request.path


class PictureUploadView(CreateView):
    """[2] upload_file.html formのテンプレートを活用する"""

    model = UploadFile
    fields = '__all__'
    template_name = 'upload_file.html'

    def form_valid(self, form):
        """
        投稿されたファイルのファイル名を取得して file_name 属性に格納する

        :param form:　upload.htmlのテンプレートフォーム
            　　 instance:データベースへ保存する前のモデルインスタンス
                instance.file_name:画像ファイルの拡張子を除いた文字列
        :return:指定されたURLにリダイレクト
        """

        instance = form.save(commit=False)
        # instance.file_nameをオーバーライドしないと、フォームに入力したファイル名
        print(instance.file.name)
        idx = instance.file.name.rfind('.')
        instance.file_name = instance.file.name[:idx]
        instance.save()
        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class PictureList(ListView):
    """画像のid、写真，削除リンクを表示する一覧ページ"""

    model = UploadFile
    template_name = 'list_file.html'


class PictureDeleteView(DeleteView):
    """画像を削除するページ"""

    model = UploadFile
    template_name = 'delete_file.html'
    success_url = reverse_lazy('pictures:picture_list')


class PictureDetailView(DetailView):
    """詳細情報を表示するページ"""

    model = UploadFile
    template_name = 'detail_file.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PictureUpdateView(MyFormValidMixin, SuccessMessageMixin, UpdateView):
    """選択した画像を差し替えるページ"""

    model = UploadFile
    template_name = 'edit_file.html'
    form_class = EditForm
    success_message = '更新成功'

    def get_success_url(self):
        """成功した時は、updateページにリダイレクト
        kwargsは、単体モデルインスタンスのid
        """

        print(self.object.id, "☆id", sep=":")
        return reverse_lazy('pictures:picture_edit', kwargs={'pk': self.object.id})

    def get_success_message(self, cleaned_data):
        """
        更新時のメッセージを表示
        :param cleaned_data:'file(InMemoryUploadedFile)'と'file_name'の辞書
        {'file': <InMemoryUploadedFile: IMG_2174.JPG (image/jpeg)>, 'file_name': 'rapping'}
        :return:カスタマイズした成功時のメッセージ（変更成功）
        """

        return f'id{self.object.id}:ファイル名{cleaned_data.get("file_name")}に変更しました (^^)/'

    def get_context_data(self, **kwargs):
        """
        fromに表示するタイトル、uploadするフオームクラスを戻り値として返す
        :param context["title"] :フォームに表示するタイトル名
               context["date"] :フォームに表示する現在日時 (動的に変更）
               context["upload_form"] :class UploadForm
        :return:context タイトルとモデルフォームを格納した辞書型オブジェクト
        """

        context = super().get_context_data(**kwargs)
        edit_form = EditForm()
        context['title'] = '☆変更ページです☆'
        context['date'] = f'ただいまの時刻は、{datetime.today().strftime("%Y/%m/%d %H:%M")}です'
        context['edit_form'] = edit_form
        print(context,"context☆",sep=":")
        return context

    def form_valid(self, form):
        """Mixinクラス MyFormValidMixinのmy_form_validソメッドを呼び出す"""

        return self.my_form_valid(form)

