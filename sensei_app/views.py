from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Count, Q
from django.core.paginator import Paginator

from django.views.generic.edit import CreateView
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from . import forms
from sensei_app.forms import AnswerForm

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
)

from sensei_app.models import *


class Toppage(TemplateView):
    template_name = 'sensei_app/toppage.html'


def ContactAdd(request):
    form = forms.ContactForm()

    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print("検証に成功しました。データを保存します")
            return render(request, 'sensei_app/toppage.html')
        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'sensei_app/Contact/contact_add.html', {'form': form})


class QuestionList(ListView):
    model = Question
    template_name = 'sensei_app/Question/question_list.html'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
                Q(title__icontains=query) |
                Q(content__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


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
    user = request.user

    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            print("検証に成功しました。データを保存します")
            print(user)
            if request.user.is_authenticated:
                question = form.save(commit=False)
                question.login_author = request.user
                question.save()
            return redirect('sensei_app:question_list')

        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'sensei_app/Question/add.html', {
        'form': form,

    })


def AnswerAdd(request, pk):
    form = forms.AnswerForm()
    user = request.user
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            print("検証に成功しました。データを保存します")
            answer.question = get_object_or_404(Question, pk=pk)
            if request.user.is_authenticated:
                answer.login_author = request.user
            answer.save()
            return redirect('sensei_app:question_detail', pk=pk)

        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'sensei_app/Question/answer.html', {
        'form': form,
        'question': question,
    })


def ReplyAdd(request, pk):
    form = forms.AnswerForm()
    user = request.user
    reply_to = get_object_or_404(Answer, pk=pk)
    question = reply_to.question
    question_pk = question.pk

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            print("検証に成功しました。データを保存します")
            answer.question = get_object_or_404(Question, pk=question_pk)
            answer.answer = get_object_or_404(Answer, pk=pk)
            if request.user.is_authenticated:
                answer.login_author = request.user
            answer.save()
            return redirect('sensei_app:question_detail', pk=question_pk)

        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'sensei_app/Question/reply.html', {
        'form': form,
        'question': reply_to,
    })


"""
class AnswerFormView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'sensei_app/Question/answer.html'

    def form_valid(self, form):
        answer = form.save(commit=False)
        question_pk = self.kwargs['pk']
        answer.question = get_object_or_404(Question, pk=question_pk)
        if self.request.user.is_authenticated:
            answer.login_author = self.request.user
            print("hello")
        answer.save()
        return redirect('sensei_app:question_detail', pk=question_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_pk = self.kwargs['pk']
        context['question'] = get_object_or_404(Question, pk=question_pk)
        return context

"""

# USER REGISTRATION

User = get_user_model()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'sensei_app/register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'sensei_app/toppage.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'sensei_app/register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('sensei_app/mail_template/create/subject.txt', context)
        subject = subject.strip()
        message = render_to_string('sensei_app/mail_template/create/message.txt', context)
        user.email_user(subject, message)
        return redirect('sensei_app:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'sensei_app/register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'sensei_app/register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # まだ仮登録で、他に問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


def UserDetail(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    questions = all_questions.filter(login_author=login_author)[:5]

    all_answers = Answer.objects.all()
    answers = all_answers.filter(login_author=login_author)[:5]

    return render(request, 'sensei_app/register/user_detail.html', {
        'user': login_author,
        'questions': questions,
        'answers': answers,
    })


def ActivitiesOfUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    questions = all_questions.filter(login_author=login_author)[:5]

    all_answers = Answer.objects.all()
    answers = all_answers.filter(login_author=login_author)[:5]

    return render(request, 'sensei_app/activities_of_user.html', {
        'user': login_author,
        'questions': questions,
        'answers': answers,
    })


def AllQuestionsofUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    questions = all_questions.filter(login_author=login_author)

    # Create a paginator to split your products queryset
    paginator = Paginator(questions, 15)  # Show 25 contacts per page
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    answers = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'sensei_app/Question/all_questions_of_user.html', {
        'user': login_author,
        'questions': questions,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
    })


def AllAnswersofUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)

    all_answers = Answer.objects.all()
    answers = all_answers.filter(login_author=login_author)

    # Create a paginator to split your products queryset
    paginator = Paginator(answers, 15)  # Show 25 contacts per page
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    answers = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'sensei_app/Question/all_answers_of_user.html', {
        'user': login_author,
        'answers': answers,
        'page_obj': page_obj,
        'num': num,
        'paginator':paginator,
    })


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー情報更新ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'sensei_app/register/user_update.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('sensei_app:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('sensei_app:password_change_done')
    template_name = 'sensei_app/register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'sensei_app/register/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'sensei_app/mail_template/password_reset/subject.txt'
    email_template_name = 'sensei_app/mail_template/password_reset/message.txt'
    template_name = 'sensei_app/register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('sensei_app:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'sensei_app/register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('sensei_app:password_reset_complete')
    template_name = 'sensei_app/register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'sensei_app/register/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'sensei_app/register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('sensei_app/mail_template/email_change/subject.txt', context)
        subject = subject.strip()
        message = render_to_string('sensei_app/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('sensei_app:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'sensei_app/register/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'sensei_app/register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)
