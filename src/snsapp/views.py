from django.shortcuts import render
from django.views.generic import TemplateView #テンプレートタグ
from .forms import AccountForm, AddAccountForm #ユーザーアカウントフォーム

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#ログイン
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# メール送信
from django.core.mail import send_mail
from django.conf import settings

def Login(request):
   form = AuthenticationForm()
   if request.method == 'POST':
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user = authenticate(username=username, password=password)
           if user is not None:
               login(request, user)
               return HttpResponseRedirect(reverse('home'))
   return render(request, 'login.html', {'form': form})


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('login'))


#ホーム
@login_required
def home(request):
    params = {"UserID":request.user,}
    return render(request, "home.html",context=params)

from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
   email = forms.EmailField(label='Email address')
   password1 = forms.CharField(widget=forms.PasswordInput)
   password2 = forms.CharField(widget=forms.PasswordInput)

   class Meta:
       model = User
       fields = ['email', 'password1', 'password2']

   def clean_password2(self):
       password1 = self.cleaned_data.get("password1")
       password2 = self.cleaned_data.get("password2")
       if password1 and password2 and password1 != password2:
           raise forms.ValidationError("Passwords don't match")
       return password2

   def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password1"])
       if commit:
           user.save()
       return user

#新規登録
class AccountRegistration(TemplateView):
   def __init__(self):
       self.params = {
       "AccountCreate":False,
       "custom_user_form": CustomUserCreationForm(),
       }

   def get(self,request):
       self.params["custom_user_form"] = CustomUserCreationForm()
       self.params["AccountCreate"] = False
       return render(request,"register.html",context=self.params)

   def post(self,request):
       self.params["custom_user_form"] = CustomUserCreationForm(data=request.POST)

       if self.params["custom_user_form"].is_valid():
           user = self.params["custom_user_form"].save()
           self.params["AccountCreate"] = True
       else:
           print(self.params["custom_user_form"].errors)

       return render(request,"register.html",context=self.params)
   
#    class  AccountRegistration(TemplateView):

#     def __init__(self):
#         self.params = {
#         "AccountCreate":False,
#         "account_form": AccountForm(),
#         "add_account_form":AddAccountForm(),
#         }

#     #Get処理
#     def get(self,request):
#         self.params["account_form"] = AccountForm()
#         self.params["add_account_form"] = AddAccountForm()
#         self.params["AccountCreate"] = False
#         return render(request,"register.html",context=self.params)

#     #Post処理
#     def post(self,request):
#         self.params["account_form"] = AccountForm(data=request.POST)
#         self.params["add_account_form"] = AddAccountForm(data=request.POST)

#         #フォーム入力の有効検証
#         if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
#             # アカウント情報をDB保存
#             account = self.params["account_form"].save()
#             # パスワードをハッシュ化
#             account.set_password(account.password)
#             # ハッシュ化パスワード更新
#             account.save()

#             # 下記追加情報
#             # 下記操作のため、コミットなし
#             add_account = self.params["add_account_form"].save(commit=False)
#             # AccountForm & AddAccountForm 1vs1 紐付け
#             add_account.user = account

#             # 画像アップロード有無検証
#             if 'account_image' in request.FILES:
#                 add_account.account_image = request.FILES['account_image']

#             # モデル保存
#             add_account.save()

#             # アカウント作成情報更新
#             self.params["AccountCreate"] = True

#         else:
#             # フォームが有効でない場合
#             print(self.params["account_form"].errors)

#         return render(request,"register.html",context=self.params)

# メール送信
# @login_required
def my_mail(request):
    send_mail(
        "テストメール",
        "Hello",
        'siranosuke1227@gmail.com',  # 送信元のメールアドレス
        ['CA01973085@st.kawahara.ac.jp'],               # 受信者リスト
        fail_silently=False,
    )
    
    return render(request, 'mail.html')