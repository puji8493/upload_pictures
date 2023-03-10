from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')

class LoginForm(AuthenticationForm):
    """
    LoginFormの__init__メソッドは、親クラスの__init__メソッドを呼び出し、
    LoginFormのインスタンスを初期化します。
    そして、LoginFormの各フィールド（例えば、ユーザー名やパスワード）に対して、
    CSSのクラス名を追加することで、フォームのスタイリングを変更しています。

    具体的には、self.fields.values()でLoginFormの全てのフィールドにアクセスし、
    それぞれのフィールドのwidgetのattrs属性に"form-control"というクラス名を追加しています。
    "form-control"クラスは、Bootstrapなどのフロントエンドライブラリで使用されるクラスで、
    テキストフィールドやボタンなどの要素をスタイリングするために使われます。
    このコードを使うことで、ログインフォームがより見やすく、使いやすくなります。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
