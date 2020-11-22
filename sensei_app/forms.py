from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select, EmailInput
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'content',)
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'メールアドレス',
            }),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'お問い合わせ内容',
            }),
        }
        labels = {
            'email': 'メールアドレス',
        }
        error_messages = {
            'email': {
                'invalid': ("無効なメールアドレスです"),
            },
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'author', 'login_author','category', 'content', 'poll_question', 'option_1', 'option_2', 'option_3', 'option_4', 'answered_user')

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトル',
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前(空欄にすると、自動的に「名無し」になります)',
            }),
            'login_author': forms.HiddenInput(),
            'category': Select(attrs={
                'class': 'form-control',
                'placeholder': 'カテゴリー',
            }),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '質問内容',
            }),
            'poll_question': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '日本語は難しい？簡単？',
                'row': 2,
            }),
            'option_1': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '難しい...',
            }),
            'option_2': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '簡単!',
            }),
            'option_3': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(任意)',
            }),
            'option_4': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(任意)',
            }),
        }
        labels = {
            'title': 'タイトル',
            'author': '',
            'content': '',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('author','login_author', 'content')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'answer': forms.HiddenInput(),
            'login_author': forms.HiddenInput(),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '回答内容',
            }),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('author','login_author', 'content')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'answer': forms.HiddenInput(),
            'login_author': forms.HiddenInput(),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '回答内容',
            }),
        }

#USER REGISTRATION

from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email', 'nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'