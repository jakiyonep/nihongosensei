from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.views.generic.edit import CreateView
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from . import forms
from sensei_app.forms import AnswerForm

from sensei_app.models import *


class Toppage(TemplateView):
    template_name = 'sensei_app/toppage.html'


class QuestionList(ListView):
    model = Question
    template_name = 'sensei_app/Question/question_list.html'


class QuestionDetail(DetailView):
    model = Question
    template_name = 'sensei_app/Question/question_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class QuestionCategoryView(ListView):
    model = Question
    template_name = 'sensei_app/Question/question_category_list.html'
    paginate_by = 15

    def get_queryset(self):
        question_category_slug = self.kwargs['question_category_slug']
        self.category = get_object_or_404(QuestionCategory, category_slug=question_category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_category_slug'] = self.category
        return context


def QuestionAdd(request):
    form = forms.QuestionForm()

    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            print("検証に成功しました。データを保存します")
            return render(request, 'sensei_app/toppage.html')
        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'sensei_app/Question/add.html', {'form': form})

class AnswerFormView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'sensei_app/Question/answer.html'

    def form_valid(self, form):
        answer = form.save(commit=False)
        question_pk = self.kwargs['pk']
        answer.question = get_object_or_404(Question, pk=question_pk)
        answer.save()
        return redirect('sensei_app:question_detail', pk=question_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_pk = self.kwargs['pk']
        context['question'] = get_object_or_404(Question, pk=question_pk)
        return context