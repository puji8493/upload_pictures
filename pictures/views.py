from datetime import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, FormView, View
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UploadForm, EditForm, CheckValidationForm, CheckValidationModelForm, EditByFormsForm, DeleteForm, \
    CommentForm
from accounts.forms import SignupForm, LoginForm
from .models import UploadFile, Comment
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


class CheckMyPostMixin(UserPassesTestMixin):
    """Mixinクラス　ログインユーザーの投稿かどうかを判定する"""

    raise_exception = True
    def test_func(self):
        """ログインユーザーの投稿かどうかを判定する"""

        post = UploadFile.objects.get(id=self.kwargs['pk'])
        return post.user == self.request.user

class MyFormValidMixin:
    """Mixinクラス　新規登録、編集時のファイルの処理を共通化したメソッドを定義"""

    def my_form_valid(self, form):
        """投稿されたファイル名を入力したファイル名＋日付にする"""

        instance = form.save(commit=False)
        if instance.file:
            instance.file_name = f'{instance.file_name}_{datetime.today().strftime("%Y%m%d")}'
        instance.save()
        return super().form_valid(form)


class PictureCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """[1]forms.py　class UploadForm(forms.ModelForm)を引数にとる"""

    model = UploadFile
    form_class = UploadForm
    template_name = 'top.html'

    def get_context_data(self, **kwargs):
        """
        fromに表示するタイトル、uploadするフオームクラスを戻り値として返す
        :param context["title"] :フォームに表示するタイトル名
               context["upload_form"] :class UploadForm
        :return:context タイトルとモデルフォームを格納した辞書型オブジェクト
        """

        context = super().get_context_data(**kwargs)

        context.update({
            'title': "☆画像のアップロード☆",
            'upload_form': UploadForm(),
        })
        return context

    def form_valid(self, form):
        """
        投稿されたファイルのファイル名を取得して file_name 属性に格納する
        :param form:　upload.htmlのテンプレートフォーム
            　　 instance:データベースへ保存する前のモデルインスタンス
        :return:指定されたURLにリダイレクト
        """
        """フォームのバリデーション"""
        instance = form.save(commit=False)
        instance.user_id = self.request.user.id
        instance.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        更新時のメッセージを表示
        :param cleaned_data:'file(InMemoryUploadedFile)'と'file_name'の辞書
        {'file': <InMemoryUploadedFile: IMG_2174.JPG (image/jpeg)>, 'file_name': 'rapping'}
        :return:カスタマイズした成功時のメッセージ(新規登録）
        """

        return f'id:{self.object.id} ファイルを{cleaned_data.get("file_name")}で新規登録しました☆'


    def get_success_url(self):
        """成功時にリダイレクトするURL"""

        return self.request.path


class PictureUploadView(LoginRequiredMixin, CreateView):
    """[2] upload_file.html formのテンプレートを活用する"""

    model = UploadFile
    form_class = UploadForm
    template_name = 'upload_file.html'

    def form_valid(self, form):
        """
        投稿されたファイルのファイル名を取得して file_name 属性に格納する
        :param form:　upload.htmlのテンプレートフォーム
            　　 instance:データベースへ保存する前のモデルインスタンス
        :return:指定されたURLにリダイレクト
        """
        """フォームのバリデーション"""
        instance = form.save(commit=False)
        instance.user_id = self.request.user.id
        instance.save()
        messages.success(self.request, 'ファイルをアップロードしました。')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class PictureList(ListView):
    """画像のid、写真，削除リンクを表示する一覧ページ"""

    model = UploadFile
    template_name = 'list_file.html'


class PictureDeleteView(CheckMyPostMixin, DeleteView):
    """画像を削除するページ"""

    model = UploadFile
    template_name = 'delete_file.html'
    success_url = reverse_lazy('pictures:picture_list')


class PictureDeleteByForm(CheckMyPostMixin, FormView):
    """フォームから画像を削除するページ"""

    model = UploadFile
    template_name = 'delete_file_2.html'
    form_class = DeleteForm
    success_url = reverse_lazy('pictures:picture_list')

    def form_valid(self, form):
        """フォームの入力値を取得して、画像を削除する"""

        id = form.cleaned_data['id']
        UploadFile.objects.get(id=id).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '画像を削除する'
        return context


class PictureDetailView(DetailView):
    """詳細情報を表示するページ"""

    model = UploadFile
    template_name = 'detail_file.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインしているユーザーの名前を取得して、コンテキストに渡す
        return context


class PictureUpdateView(CheckMyPostMixin, SuccessMessageMixin, UpdateView):
    """選択した画像を差し替える編集ページ
    　　modelform使用たと更新できる。forms.Formは更新できない"""

    model = UploadFile
    template_name = 'edit_file.html'
    form_class = EditForm
    success_message = '更新成功'

    def get_success_url(self):
        """成功した時は、updateページにリダイレクト
        kwargsは、単体モデルインスタンスのid
        """

        return reverse_lazy('pictures:picture_edit', kwargs={'pk': self.object.id})

    def get_success_message(self, cleaned_data):
        """
        更新時のメッセージを表示
        :param cleaned_data:'file(InMemoryUploadedFile)'とformに入力した文字列'file_name'の辞書
        {'file': <InMemoryUploadedFile: IMG_2174.JPG (image/jpeg)>, 'file_name': 'rapping'}
        :return:成功時のメッセージ
        """

        return f'id：{self.object.id},file_name: {self.object.file_name}に変更しました。フォームに入力した文字列は{cleaned_data["file_name"]}です'

    def get_context_data(self, **kwargs):
        """
        fromに表示するタイトル、uploadするフオームクラスを戻り値として返す
        :param:context["id"] :フォームに表示するオブジェクトのid
               context["title"] :フォームに表示するタイトル名
               context["date"] :フォームに表示する現在日時
               context["upload_form"] :class UploadForm
        :return:context タイトルとモデルフォームを格納した辞書型オブジェクト
        """

        context = super().get_context_data(**kwargs)
        edit_form = EditForm()
        context['id'] = self.object.id
        context['title'] = 'の変更ページです'
        context['date'] = f'ただいまの時刻は、{datetime.today().strftime("%Y/%m/%d %H:%M")}です'
        context['edit_form'] = edit_form
        return context

    def form_valid(self, form):
        """
        投稿されたファイルのファイル名を取得して file_name 属性に格納する
        :param form:　upload.htmlのテンプレートフォーム
            　　 instance:データベースへ保存する前のモデルインスタンス
        :return:指定されたURLにリダイレクト
        """
        """フォームのバリデーション"""
        instance = form.save(commit=False)
        instance.user_id = self.request.user.id
        instance.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     """form_validメソッドだけを定義したMixinクラス(MyFormValidMixin)を呼び出す"""
    #
    #     return self.my_form_valid(form)


class CheckValidationView(LoginRequiredMixin, FormView):
    """form.Formsクラスを継承したクラス"""

    template_name = 'check_validation.html'
    form_class = CheckValidationForm
    success_url = reverse_lazy('pictures:picture_clean')

    def form_valid(self, form):
        """
        フォームの送信が成功した時の処理

        :param: file:フォームで登録した画像
                file_name:フォームで入力したファイル名
        :return:

        """

        file = form.cleaned_data.get("file")
        file_name = form.cleaned_data.get("file_name")
        user = self.request.user
        data = {'file': file, 'file_name': file_name, 'user': user}
        instance = UploadFile(**data)
        instance.save()
        return super().form_valid(form)


class CheckValidationViewByModelForm(LoginRequiredMixin, CreateView):
    """
    モデルフォームを使ってフォームのバリデーションを確認する


    """
    model = UploadFile
    template_name = 'check_validation_model.html'
    form_class = CheckValidationModelForm
    success_url = reverse_lazy('pictures:picture_clean_model')

    def form_valid(self, form):
        """フォームのバリデーション"""
        instance = form.save(commit=False)
        instance.user_id = self.request.user.id
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """フォームのバリデーション"""
        print("Viewのform_invlidメソッドの出力", form.errors, sep="：")
        return super().form_invalid(form)


class EditView(CheckMyPostMixin, View):
    """ファイルを編集"""

    def get(self, request, *args, **kwargs):
        edit_form = EditByFormsForm()
        return render(request, 'edit_file_3.html', context={'edit_form': edit_form})

    def post(self, request, *args, **kwargs):
        edit_form = EditByFormsForm(request.POST, request.FILES)
        if edit_form.is_valid():
            data = edit_form.cleaned_data
            print(data['file'], data['file_name'])
            instance = UploadFile.objects.get(id=self.kwargs['pk'])
            print(instance, '変更前のinsetanceです')
            instance.file = data['file']
            instance.file_name = data['file_name']
            instance.save()
            print(instance, '変更後のinsetanceです')
        return render(request, 'edit_file_3.html', context={'edit_form': edit_form})
        # reverse razyは'__proxy__' object has no attribute 'get'


class EditViewByForm(CheckMyPostMixin, FormView):
    """ファイルを編集するFromViewクラス"""

    model = UploadFile
    template_name = 'edit_file_2.html'
    form_class = EditByFormsForm
    success_url = reverse_lazy('pictures:picture_list')

    def get_initial(self):
        """初期値を設定する"""
        instance = UploadFile.objects.get(id=self.kwargs['pk'])
        print(instance.file.url, "fileのulr")
        return {'file': instance.file, 'file_name': instance.file_name, 'file_url': instance.file.url}

    def form_valid(self, form):
        """フォームのバリデーション"""
        data = form.cleaned_data
        print(data['file'], data['file_name'])
        instance = UploadFile.objects.get(id=self.kwargs['pk'])
        print(instance)
        instance.file = data['file']
        instance.file_name = data['file_name']
        instance.save()
        return super().form_valid(form)


class CommentView(LoginRequiredMixin, CreateView):
    """コメントを登録するViewクラス"""

    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def form_valid(self, form):
        """フォームのバリデーション"""
        uploadfile_pk = self.kwargs['pk']
        uploadfile = get_object_or_404(UploadFile, pk=uploadfile_pk)

        # comment 変数を初期化するために、 comment = None を追加しています。
        # また、 if self.request.user.is_authenticated 文を追加し、
        # ログインしている場合のみ comment 変数に値を設定するようにしました。

        comment = None  # 変数を初期化する
        if self.request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.target = uploadfile
            comment.save()
        return redirect('pictures:picture_detail', pk=uploadfile_pk)


class Login(LoginView):
    """ログインページ"""

    template_name = 'login.html'
    form_class = LoginForm


class Logout(LogoutView):
    """ログアウトページ"""

    template_name = 'logout.html'


class SignUp(CreateView):
    """ユーザー登録ページ"""

    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('pictures:picture_list')

    def form_valid(self, form):
        """ユーザー登録"""
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

    # def form_valid(self, form):
    #     """ユーザー登録"""
    #     user = form.save()
    #     login(self.request, user)
    #     self.object = user
    #     messages.info(self.request, 'ユーザー登録が完了しました。')
    #     return HttpResponseRedirect(self.get_success_url())
