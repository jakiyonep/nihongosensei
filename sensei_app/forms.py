from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select
from .models import Question, Answer



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'author', 'category', 'content')
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトル',
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'category': Select(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '質問内容',
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
        fields = ('author', 'content')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '回答内容',
            }),
        }

