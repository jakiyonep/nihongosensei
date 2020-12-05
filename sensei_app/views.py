from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Count, Q
from django.core.paginator import Paginator
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.generic.edit import CreateView
from django.http import Http404, JsonResponse
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
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, EmailChangeForm,
    QuestionForm, AnswerForm,
)
from django.contrib.auth.decorators import login_required
from sensei_app.models import *



# SiteDesc

class SiteDescView(TemplateView):
    template_name = "sensei_app/sitedesc.html"

class Toppage(TemplateView):
    template_name = 'sensei_app/toppage.html'

# Contact

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

# Markdown

def Markdown_Exp(request):
    htmltags = MarkdownExpModel.objects.all()

    context={
        "htmltags": htmltags
    }

    return render(request, 'sensei_app/markdownexp.html', context)

# RegisterPerk

def RegisterPerkList(request):
    perks = RegisterPerk.objects.all()

    context = {
        "perks": perks
    }

    return render(request, "sensei_app/register/register_perk.html", context)

def TermsConditionsView(request):
    selected_terms = get_object_or_404(TermsConditions, number=1)


    context = {
        'terms':selected_terms
    }

    return render(request, "sensei_app/termsandconditions.html", context)

def PrivacyPolicyView(request):
    selected_terms = get_object_or_404(TermsConditions, number=2)
    context = {
        'policy': selected_terms
    }

    return render(request, "sensei_app/privacypolicy.html", context)

# Question

def QuestionList(request):
    question_list = Question.objects.all()
    query = request.GET.get('q')

    if query:
        question_list = Question.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__icontains=query)
        ).distinct()
    paginator = Paginator(question_list, 14)
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'sensei_app/Question/question_list.html', {
        'question_list': question_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'query': query,
    })

def QuestionDetail(request, pk):
    context = {}
    question = get_object_or_404(Question,pk=pk)
    user = request.user
    answers = Answer.objects.all()
    answers = answers.filter(question=question)

    if question.answered_user.filter(pk=user.pk).exists():
        context['already_voted'] = 1

    if request.method == 'POST':
        selected_sort = request.POST['selected_sort']

        if selected_sort == 'likes':
            answers = answers\
                    .annotate(num_likes=Count('likes'))\
                    .order_by('-num_likes')
        elif selected_sort == 'new':
            answers = answers.order_by('-created_at')
        elif selected_sort == 'old':
            answers = answers.order_by('created_at')


        context = {
            'question': question,
            'answers': answers,
        }

        html = render_to_string('sensei_app/Question/comments.html', context, request=request)

        return JsonResponse({'answers_sort': html})

    context ={
        'question': question,
        'answers': answers,
    }

    return render(request, 'sensei_app/Question/question_detail.html', context)

def QuestionCategoryView(request, question_category_slug):
    category_slug = question_category_slug
    selected_category = get_object_or_404(QuestionCategory, category_slug=category_slug)
    all_question = Question.objects.all()
    question_list = all_question.filter(category__category_name=selected_category)

    paginator = Paginator(question_list, 14)
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'sensei_app/Question/question_list.html', {
        'question_list': question_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'selected_category': selected_category

    })

def QuestionAdd(request):
    form = forms.QuestionForm()
    user = request.user

    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        if "button" in request.POST:
            if form.is_valid():
                if request.user.is_authenticated:
                    question = form.save(commit=False)
                    question.login_author = request.user
                    question.save()
                else:
                    form.save()
                return redirect('sensei_app:question_list')

            else:
                print(form.errors)


    return render(request, 'sensei_app/Question/add.html', {
        'form': form,
    })

def QuestionAddition(request):
    context={}
    if request.is_ajax():
        addition_content = request.POST['addition_content']
        question_id = request.POST['addition_question_id']
        question = get_object_or_404(Question, pk=question_id)
        question.addition = addition_content
        question.save()
        question_category_slug = question.category.category_slug
        context = {
            'addition_content': addition_content,
            'question_category_slug': question_category_slug,
        }

        html = render_to_string('sensei_app/Question/content_addition.html', context, request=request)

        return JsonResponse({'addition':html})

def QuestionPollVote(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if request.is_ajax():
            question_id = request.POST['question_id']
            selected_option = request.POST['selected_option']
            question = get_object_or_404(Question, pk=question_id)
            if not question.answered_user.filter(pk=user.pk).exists():
                question.answered_user.add(user)
                print('first time')
                if selected_option == "1":
                    question.option_1_count += 1
                if selected_option == "2":
                    question.option_2_count += 1
                if selected_option == "3":
                    question.option_3_count += 1
                if selected_option == "4":
                    question.option_4_count += 1

                question.save()
                question_category_slug = question.category.category_slug
                context = {
                    'question': question,
                    'question_category_slug': question_category_slug,
                    'ajax_requested': 1,
                }

                option_1_count = question.option_1_count
                option_2_count = question.option_2_count
                option_3_count = question.option_3_count
                option_4_count = question.option_4_count
                option_1_percentage = 0
                option_2_percentage = 0
                option_3_percentage = 0
                option_4_percentage = 0
                total = option_1_count + option_2_count + option_3_count + option_4_count

                if not option_1_count == 0:
                    option_1_percentage = round(option_1_count / total * 100)
                if not option_2_count == 0:
                    option_2_percentage = round(option_2_count / total * 100)
                if not option_3_count == 0:
                    option_3_percentage = round(option_3_count / total * 100)
                if not option_4_count == 0:
                    option_4_percentage = round(option_4_count / total * 100)

                context["poll_total"] = total
                context["option_1_percentage"] = option_1_percentage
                context["option_2_percentage"] = option_2_percentage
                context["option_3_percentage"] = option_3_percentage
                context["option_4_percentage"] = option_4_percentage

                html = render_to_string('sensei_app/Question/content_poll.html', context, request=request)
                already_answered = 1

                return JsonResponse({
                    'poll_vote': html,
                    "option_1_percentage": option_1_percentage,
                    "option_2_percentage": option_2_percentage,
                    "option_3_percentage": option_3_percentage,
                    "option_4_percentage": option_4_percentage,
                })
            else:
                return redirect('https://google.co.jp')

    else:
        return redirect('https://google.co.jp')

@login_required
def QuestionDelete(request,pk):
    comment = get_object_or_404(Question, pk=pk)
    comment.delete()
    print("heelo")

    return redirect('sensei_app:question_list')

def AnswerAdd(request):
    context={}
    if request.is_ajax():
        login_author = None
        author = request.POST['answer_author']
        answer_content = request.POST['answer_content']
        question_id = request.POST['question_id']
        question = get_object_or_404(Question, pk=question_id)
        if request.user.is_authenticated:
            login_author = request.user
        answer = Answer(
            question = question,
            author = author,
            content = answer_content,
            created_at = timezone.now(),
            login_author = login_author,
        )
        answer.save()

        all_answers = Answer.objects.all()
        answers = all_answers.filter(question=question)
        ajax_selected_sort = request.POST['ajax_selected_sort']

        if ajax_selected_sort == 'likes':
            answers = answers\
                    .annotate(num_likes=Count('likes'))\
                    .order_by('-num_likes')
        elif ajax_selected_sort == 'new':
            answers = answers.order_by('-created_at')
        elif ajax_selected_sort == 'old':
            answers = answers.order_by('created_at')

        context = {
            'answers': answers,
            'question': question,
        }

        html = render_to_string('sensei_app/Question/comments.html', context, request=request)

        return JsonResponse({'form':html})

@login_required
def AnswerLike(request):
    context ={}
    user = request.user
    answer_id = request.POST['answer_id']
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        if answer.likes.filter(pk=user.pk).exists():
            answer.likes.remove(user)
            is_liked = False
        else:
            answer.likes.add(user)
            is_liked = True
        context = {
            'answer': answer,
            'is_liked': is_liked,
            'total_likes': answer.total_likes()
        }
    if request.is_ajax():
        html = render_to_string('sensei_app/Question/answer_like.html', context, request=request)
        return JsonResponse({'form':html})

@login_required()
def AnswerDelete(request,pk):
    answer = get_object_or_404(Answer, pk=pk)
    question = answer.question
    question_pk = question.pk

    answer.delete()

    return redirect("sensei_app:question_detail", pk=question_pk )

def ReplyAdd(request):
    context={}
    if request.is_ajax():
        login_author = None
        author = request.POST['reply_author']
        reply_content = request.POST['reply_content']
        answer_id = request.POST['answer_id']
        answer = get_object_or_404(Answer, pk=answer_id)
        replies = Reply.objects.all()
        replies = replies.filter(answer=answer)
        request_user = request.user
        if request.user.is_authenticated:
            login_author = request.user
        reply = Reply(
            answer = answer,
            author = author,
            content = reply_content,
            created_at = timezone.now(),
            login_author = login_author,
        )
        reply.save()

        all_replies = Reply.objects.all()
        ajax_replies = all_replies.filter(answer=answer)
        context = {
            'ajax_replies': ajax_replies,
            'replies': replies,
            'ajax_question':answer.question,
            'answer_id': answer_id,
            'request_user': request_user,
            'reply_author': author,
            'answer_author': answer.author,
            'answer_login_author': answer.login_author,
        }

        html = render_to_string('sensei_app/Question/ajax_replies.html', context)

        return JsonResponse({'form':html})

@login_required()
def ReplyDelete(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    question = reply.answer.question
    question_pk = question.pk
    reply.delete()

    return redirect("sensei_app:question_detail", pk=question_pk)

# EXAM

def JLTCTTop(request):
    query = request.GET.get('q')
    all_exam = jltct.objects.all()

    if query:
        all_exam = jltct.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(section__section__icontains=query) |
            Q(tag__tag__icontains=query)
        )

    society = all_exam.filter(section__section_slug="society")
    language_society = all_exam.filter(section__section_slug="languagesociety")
    language_psychology = all_exam.filter(section__section_slug="languagepsychology")
    language_education = all_exam.filter(section__section_slug="languageeducation")
    language = all_exam.filter(section__section_slug="language")

    context={
        "society": society,
        "language": language,
        "language_society": language_society,
        "language_psychology": language_psychology,
        "language_education": language_education,
        "query": query,

     }

    return render(request, 'sensei_app/Exam/jltct_top.html', context)

def JLTCTNoteDetail(request, title_slug):
    note = get_object_or_404(jltct,title_slug=title_slug)

    context ={
        "note": note,
    }

    return render(request, "sensei_app/Exam/jltct_note_detail.html", context)

def ExamExpDetail(request, year, section, question_num):
    exp_list = ExamExp.objects.filter(year=year, section=section, question_num=question_num)
    year = year
    section = section
    section_roman = None
    section_beginning = 0
    section_end = 0


    if section == 1:
        section_roman = 'I'
    elif section == 2:
        section_roman = 'II'
    elif section == 3:
        section_roman = 'III'

    question_num = question_num

    section_previous = section - 1
    section_next = section + 1
    question_num_previous = question_num - 1
    question_num_next = question_num + 1

    if section == 1:
        if question_num == 1:
            section_beginning = 1
        if question_num == 15:
            section_end = 1
    elif section == 2:
        if question_num == 1:
            section_beginning = 1
        if question_num == 6:
            section_end = 1
    elif section == 3:
        if question_num == 1:
            section_beginning = 1
        if question_num == 16:
            section_end = 1

    print('------------------------------------------')
    print(section_beginning)
    print('------------------------------------------')
    print(section_end)
    print('------------------------------------------')
    context = {
        "exp_list": exp_list,
        'year': year,
        'section': section,
        'section_roman': section_roman,
        'question_num': question_num,
        'section_previous': section_previous,
        'section_next': section_next,
        'question_num_next': question_num_next,
        'question_num_previous':question_num_previous,
        'section_beginning': section_beginning,
        'section_end': section_end,
    }

    if len(exp_list) == 0:
        context['none'] = 1
    return render(request, 'sensei_app/Exam/Exp/exp_detail.html', context)

@login_required
def NoteLike(request):
    user = request.user
    note_id = request.POST['note_id']
    note = get_object_or_404(jltct, pk=note_id)
    if request.method == 'POST':
        if note.likes.filter(pk=user.pk).exists():
            note.likes.remove(user)
            is_liked = False
        else:
            note.likes.add(user)
            is_liked = True
        context = {
            'note': note,
            'is_liked': is_liked,
            'total_likes': note.total_likes()
        }
    if request.is_ajax():
        html = render_to_string('sensei_app/Exam/like.html', context, request=request)
        return JsonResponse({'form':html})

@login_required
def JltctCommentAdd(request):
    context={}
    if request.is_ajax():
        comment_content = request.POST['comment_content']
        note_id = request.POST['note_id']
        note = get_object_or_404(jltct, pk=note_id)
        comments = JltctComment.objects.all()
        comments = comments.filter(note=note)
        login_author = request.user
        comment = JltctComment(
            note = note,
            login_author=login_author,
            content = comment_content,
            created_at = timezone.now(),
        )
        comment.save()
        all_comments = JltctComment.objects.all()
        ajax_comments = all_comments.filter(note=note)
        context = {
            'ajax_comments': ajax_comments,
            'note': note
        }

        html = render_to_string('sensei_app/Exam/comments.html', context)

        return JsonResponse({'form':html})

@login_required
def JltctCommentDelete(request, pk):
    comment = get_object_or_404(JltctComment, pk=pk)
    note = comment.note
    note_title_slug = note.title_slug
    comment.delete()

    return redirect("sensei_app:note_detail", title_slug=note_title_slug)

@login_required
def JltctReplyDelete(request, pk):
    reply = get_object_or_404(JltctReply, pk=pk)
    note = reply.comment.note
    note_title_slug = note.title_slug
    reply.delete()

    return redirect("sensei_app:note_detail", title_slug=note_title_slug)

@login_required
def JltctReplyAdd(request):
    context={}
    if request.is_ajax():
        reply_content = request.POST['reply_content']
        comment_id = request.POST['comment_id']
        comment = get_object_or_404(JltctComment, pk=comment_id)
        login_author = request.user
        reply = JltctReply(
            comment = comment,
            login_author=login_author,
            content = reply_content,
            created_at = timezone.now(),
        )
        reply.save()
        all_replies = JltctReply.objects.all()
        ajax_replies = all_replies.filter(comment=comment)
        context = {
            'ajax_replies': ajax_replies,
            'reply': reply,
            'comment': comment,
        }

        html = render_to_string('sensei_app/Exam/replies.html', context)

        return JsonResponse({'form':html})

def JLTCTTagNotes(request,tag_slug):
    selected_tag = get_object_or_404(jltcttag,tag_slug=tag_slug)
    selected_notes = jltct.objects.filter(tag=selected_tag)

    society = selected_notes.filter(section__section_slug="society")
    language_society = selected_notes.filter(section__section_slug="languagesociety")
    language_psychology = selected_notes.filter(section__section_slug="languagepsychology")
    language_education = selected_notes.filter(section__section_slug="languageeducation")
    language = selected_notes.filter(section__section_slug="language")

    context = {
        "selected_tag": selected_tag,
        "selected_notes": selected_notes,
        "society": society,
        "language": language,
        "language_society": language_society,
        "language_psychology": language_psychology,
        "language_education": language_education,
    }

    return render(request, "sensei_app/Exam/jltct_tag_notes.html", context)


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
    questions = all_questions.filter(login_author=login_author)[:6]
    all_questions_num = all_questions.filter(login_author=login_author).count()

    all_answers = Answer.objects.all()
    answers = all_answers.filter(login_author=login_author)[:6]
    all_answers_num = all_answers.filter(login_author=login_author).count()

    all_exam = jltct.objects.all()

    society = all_exam.filter(section__section_slug="society").filter(likes=request.user)
    language_society = all_exam.filter(section__section_slug="languagesociety").filter(likes=request.user)
    language_psychology = all_exam.filter(section__section_slug="languagepsychology").filter(likes=request.user)
    language_education = all_exam.filter(section__section_slug="languageeducation").filter(likes=request.user)
    language = all_exam.filter(section__section_slug="language").filter(likes=request.user)



    context={
        "society": society,
        "language": language,
        "language_society": language_society,
        "language_psychology": language_psychology,
        "language_education": language_education,
        'user': login_author,
        'question_list': questions,
        'answer_list': answers,
        'all_questions_num': all_questions_num,
        'all_answers_num': all_answers_num,
    }

    return render(request, 'sensei_app/register/user_detail.html', context)

def ActivitiesOfUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    all_questions_num = all_questions.filter(login_author=login_author).count()
    questions = all_questions.filter(login_author=login_author)[:6]

    all_answers = Answer.objects.all()
    all_answers_num = all_answers.filter(login_author=login_author).count()
    answers = all_answers.filter(login_author=login_author)[:6]

    all_exam = jltct.objects.all()

    society = all_exam.filter(section__section_slug="society")
    language_society = all_exam.filter(section__section_slug="languagesociety")
    language_psychology = all_exam.filter(section__section_slug="languagepsychology")
    language_education = all_exam.filter(section__section_slug="languageeducation")
    language = all_exam.filter(section__section_slug="language")

    context = {
        "society": society,
        "language": language,
        "language_society": language_society,
        "language_psychology": language_psychology,
        "language_education": language_education,
        'user': login_author,
        'question_list': questions,
        'answer_list': answers,
        'all_questions_num': all_questions_num,
        'all_answers_num': all_answers_num,
    }

    return render(request, 'sensei_app/activities_of_user.html', context)

def AllQuestionsofUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    questions = all_questions.filter(login_author=login_author)

    paginator = Paginator(questions, 14)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'sensei_app/Question/all_questions_of_user.html', {
        'user': login_author,
        'question_list': questions,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
    })

def AllAnswersofUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)

    all_answers = Answer.objects.all()
    answers = all_answers.filter(login_author=login_author)

    paginator = Paginator(answers, 14)
    page = request.GET.get('page')
    answers = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'sensei_app/Question/all_answers_of_user.html', {
        'user': login_author,
        'answer_list': answers,
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
