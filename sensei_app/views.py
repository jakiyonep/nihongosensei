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
from django.http import HttpResponseBadRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from sensei_app.models import *



########### SiteDesc

def SiteDescView(request):
    current_date = timezone.now()
    context = {
        'current_date': current_date,
    }
    return render(request, "sensei_app/SiteInfo/sitedesc.html", context)

class Toppage(TemplateView):
    template_name = 'sensei_app/toppage.html'

########### Contact

def ContactAdd(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print("検証に成功しました。データを保存します")
            return render(request, 'sensei_app/toppage.html')
        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'sensei_app/Contact/contact_add.html', {'form': form})

########### Markdown

def Markdown_Exp(request):
    htmltags = MarkdownExpModel.objects.all()

    context={
        "htmltags": htmltags
    }

    return render(request, 'sensei_app/Snippet/markdownexp.html', context)

########### RegisterPerk

def RegisterPerkList(request):
    perks = RegisterPerk.objects.all()

    context = {
        "perks": perks
    }

    return render(request, "sensei_app/Register/register_perk.html", context)

def TermsConditionsView(request):
    selected_terms = get_object_or_404(TermsConditions, number=1)


    context = {
        'terms':selected_terms
    }

    return render(request, "sensei_app/Register/termsandconditions.html", context)

def PrivacyPolicyView(request):
    selected_terms = get_object_or_404(TermsConditions, number=2)
    context = {
        'policy': selected_terms
    }

    return render(request, "sensei_app/privacypolicy.html", context)

########### Question

def QuestionList(request):
    service_name = "質問"
    question_list = Question.objects.all()
    query = request.GET.get('q')
    result = 0
    if query:
        query_dict = query.split()
        result = 1
        for query_each in query_dict:
            question_list = question_list.filter(
                Q(title__icontains=query_each) |
                Q(content__icontains=query_each) |
                Q(author__icontains=query_each)
            ).distinct()
    paginator = Paginator(question_list, 14)
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    context = {
        'question_list': question_list,
        'page_obj': page_obj,
        'num': num,
        'result': result,
        'paginator': paginator,
        'query': query,
        'service_name':service_name,
    }

    return render(request, 'sensei_app/Question/question_list.html', context)

def QuestionDetail(request, pk):
    context = {}
    question = get_object_or_404(Question,pk=pk)
    user = request.user
    answers = Answer.objects.all()
    answers = answers.filter(question=question)

    if question.answered_user.filter(pk=user.pk).exists():
        context['already_voted'] = 1

    if request.method == 'POST':
        if request.POST.get("comment_submit"):
            selected_sort = request.POST['selected_sort']

            if selected_sort == 'likes':
                answers = answers\
                        .annotate(num_likes=Count('likes'))\
                        .order_by('-num_likes')
            elif selected_sort == 'new':
                answers = answers.order_by('-created_at')
            elif selected_sort == 'old':
                answers = answers.order_by('created_at')


            context['question'] = question
            context['answers'] = answers

            html = render_to_string('sensei_app/Question/Detail/Answers/comments.html', context, request=request)

            return JsonResponse({'comment_sort': html})

    context['question'] = question
    context['answers'] = answers

    return render(request, 'sensei_app/Question/Detail/question_detail.html', context)

def QuestionCategoryView(request, question_category_slug):
    service_name = "質問"
    category_slug = question_category_slug
    selected_category = get_object_or_404(QuestionCategory, category_slug=category_slug)
    all_question = Question.objects.all()
    question_list = all_question.filter(category__category_name=selected_category)

    paginator = Paginator(question_list, 14)
    page = request.GET.get('page')
    question_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    context = {
        'service_name': service_name,
        'question_list': question_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'selected_category': selected_category,
        'result': 1,
    }



    return render(request, 'sensei_app/Question/question_list.html', context)

def QuestionAdd(request):
    form = QuestionForm()
    user = request.user
    if request.method == 'POST':
        form = QuestionForm(request.POST)
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
            'question': question,
            'addition_content': addition_content,
            'question_category_slug': question_category_slug,
        }

        html = render_to_string('sensei_app/Question/Detail/Snippet/content_addition.html', context, request=request)

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


                context["already_voted"] = 1
                context = {
                    'question': question,
                    'question_category_slug': question_category_slug,
                    'ajax_requested': 1,
                }

                html = render_to_string('sensei_app/Question/Detail/Snippet/content_poll.html', context, request=request)
                already_answered = 1
                return JsonResponse({
                    'poll_vote': html,
                })
            return HttpResponse('')

    else:
        return HttpResponse('')

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
        ajax_selected_sort = "new"

        if request == 'POST':
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

        html = render_to_string('sensei_app/Question/Detail/Answers/comments.html', context, request=request)

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
        html = render_to_string('sensei_app/Question/Detail/Answers/answer_like.html', context, request=request)
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
            'answer':answer,
        }

        html = render_to_string('sensei_app/Question/Detail/Answers/ajax_replies.html', context)

        return JsonResponse({'form':html})

@login_required()
def ReplyDelete(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    question = reply.answer.question
    question_pk = question.pk
    reply.delete()

    return redirect("sensei_app:question_detail", pk=question_pk)

########### EXAM

def JLTCTTop(request):
    query = request.GET.get('q')
    result = 0
    all_exam = jltct.objects.all()
    note_list = all_exam
    note_search = 0
    exp_search = 0

    if query:
        result = 1
        note_search = 1
        query_dict = query.split()
        for query_each in query_dict:
            note_list = note_list.filter(
                Q(title__icontains=query_each) |
                Q(content__icontains=query_each) |
                Q(category__category__icontains=query_each) |
                Q(tag__tag__icontains=query_each)
            )
    context={
        "note_list": note_list,
        "query": query,
        "note_search": note_search,
      }

    exp_query = request.GET.get('exp_q')
    exp_list = ExamExp.objects.all()
    if exp_query:
        result = 1
        exp_search = 1
        exp_query_dict = exp_query.split()
        for exp_query_each in exp_query_dict:
            exp_list = exp_list.filter(
                Q(question_head__icontains=exp_query_each) |
                Q(explanation__icontains=exp_query_each) |
                Q(answer_1__icontains=exp_query_each) |
                Q(answer_2__icontains=exp_query_each) |
                Q(answer_3__icontains=exp_query_each) |
                Q(answer_4__icontains=exp_query_each) |
                Q(answer_5__icontains=exp_query_each) |
                Q(after_exp__icontains=exp_query_each)
            )

        context['exp_query'] = exp_query
        context['exp_list'] = exp_list
    context["exp_search"] = exp_search
    context['result'] = result
    context['service_name'] = "ノート"

    return render(request, 'sensei_app/JLTCT/jltct_top.html', context)

def JLTCTCategoryNotes(request,category_slug):
    selected_category = get_object_or_404(jltctcategory, category_slug=category_slug)
    note_list = jltct.objects.filter(category=selected_category)
    service_name = "ノート"


    context = {
        "selected_category": selected_category,
        "note_list": note_list,
        "service_name": service_name,
        "result": 1,
        "note_search": 1,
    }

    return render(request, "sensei_app/JLTCT/jltct_top.html", context)

def JLTCTTagNotes(request,tag_slug):
    selected_tag = get_object_or_404(jltcttag,tag_slug=tag_slug)
    note_list = jltct.objects.filter(tag=selected_tag)
    service_name = "ノート"


    context = {
        "selected_tag": selected_tag,
        "note_list": note_list,
        "service_name": service_name,
        "result": 1,
        "note_search": 1,
     }

    return render(request, "sensei_app/JLTCT/jltct_top.html", context)

def JLTCTNoteDetail(request, title_slug):
    note = get_object_or_404(jltct,title_slug=title_slug)

    context ={
        "note": note,
    }

    return render(request, "sensei_app/JLTCT/Note/jltct_note_detail.html", context)

def ExamTagList(request,tag_slug):
    selected_tag = get_object_or_404(ExamTags,tag_slug=tag_slug)
    exp_list = ExamExp.objects.filter(tag=selected_tag)
    service_name = "過去問解説"

    context = {
        "selected_tag": selected_tag,
        "exp_list": exp_list,
        "exp_search": 1,
        "result": 1,
        "service_name": service_name,
    }

    return render(request, "sensei_app/JLTCT/jltct_top.html", context)

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
    else:
        for exp in exp_list:
            if exp.public == False:
                context['none'] = 1

    return render(request, 'sensei_app/JLTCT/Exp/exp_detail.html', context)

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
        html = render_to_string('sensei_app/JLTCT/Note/like.html', context, request=request)
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

        html = render_to_string('sensei_app/JLTCT/Note/Comments/comments.html', context)

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

        html = render_to_string('sensei_app/JLTCT/Note/Comments/replies.html', context)

        return JsonResponse({'form':html})


########### Material

def MaterialTop(request):
    materials = Material.objects.all()
    service_name = "教材"
    result = 0
    query = request.GET.get('q')

    if query:
        result = 1
        query_dict = query.split()
        for query_each in query_dict:
            materials = materials.filter(
                Q(title__icontains=query_each) |
                Q(category__category__icontains=query_each) |
                Q(tag__tag__icontains=query_each) |
                Q(description__icontains=query_each)
            ).distinct()
            print(query_each)
    paginator = Paginator(materials, 20)
    page = request.GET.get('page')
    materials = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    context = {
        'materials': materials,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'query': query,
        'result': result,
        'service_name': service_name,
    }

    return render(request, 'sensei_app/Material/toppage.html', context)

def MaterialCategoryList(request, category_slug):
    service_name = "教材"
    all_materials = Material.objects.all()
    selected_category = get_object_or_404(MaterialCategory, category_slug=category_slug)

    materials = all_materials.filter(category=selected_category)

    context = {
        'selected_category': selected_category,
        'materials': materials,
        'result': 1,
        'service_name':service_name,
    }

    return render(request, 'sensei_app/Material/toppage.html', context)

def MaterialTagList(request, tag_slug):
    service_name = "教材"
    all_materials = Material.objects.all()
    selected_tag = get_object_or_404(MaterialTag, tag_slug=tag_slug)

    materials = all_materials.filter(tag=selected_tag)

    context = {
        'selected_tag': selected_tag,
        'materials': materials,
        'result': 1,
        'service_name': service_name,
    }

    return render(request, 'sensei_app/Material/toppage.html', context)

class MaterialUpload(generic.CreateView):
    model = Material
    form_class = MaterialUploadForm
    template_name = 'sensei_app/Material/upload.html'
    success_url = reverse_lazy('sensei_app:material_top')

    def form_valid(self, form):
        material = form.save(commit=False)
        material.uploader = self.request.user
        return super(MaterialUpload,self).form_valid(form)

########### Blog

def BlogTop(request):
    result = 0
    service_name = "きまま"
    blog_list = Blog.objects.all()

    query = request.GET.get('q')

    if query:
        result = 1
        query_dict = query.split()
        for query_each in query_dict:
            blog_list = blog_list.filter(
                Q(title__icontains=query_each) |
                Q(category__category__icontains=query_each) |
                Q(tag__tag__icontains=query_each) |
                Q(content__icontains=query_each)
            ).distinct()
    paginator = Paginator(blog_list, 20)
    page = request.GET.get('page')
    blog_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    context = {
        'blog_list': blog_list,
        'query': query,
        'page': page,
        'page_obj': page_obj,
        'result': result,
        'service_name': service_name,
    }


    return render(request, "sensei_app/Blog/blog_top.html", context)

def BlogCategoryList(request, category_slug):
    service_name = "きまま"
    selected_category = get_object_or_404(BlogCategory, category_slug=category_slug)
    blog_list = Blog.objects.filter(category=selected_category)

    paginator = Paginator(blog_list, 20)
    page = request.GET.get('page')
    blog_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    context = {
        'blog_list': blog_list,
        'result': 1,
        'service_name': service_name,
        'page': page,
        'page_obj': page_obj,
        'selected_category': selected_category
    }

    return  render(request, 'sensei_app/Blog/blog_top.html', context)


def BlogTagList(request, tag_slug):
    service_name = "きまま"
    selected_tag = get_object_or_404(BlogTag, tag_slug=tag_slug)
    blog_list = Blog.objects.filter(tag=selected_tag)

    paginator = Paginator(blog_list, 20)
    page = request.GET.get('page')
    blog_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    context = {
        'blog_list': blog_list,
        'result': 1,
        'service_name': service_name,
        'page': page,
        'page_obj': page_obj,
        'selected_tag': selected_tag
    }

    return render(request, 'sensei_app/Blog/blog_top.html', context)


def BlogDetail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    context = {
        "blog": blog
    }

    return render(request, "sensei_app/Blog/blog_detail.html", context)


########### USER REGISTRATION

User = get_user_model()

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'sensei_app/UserInfo/login.html'

class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'sensei_app/toppage.html'

class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'sensei_app/Register/user_create.html'
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
    template_name = 'sensei_app/Register/user_create_done.html'

class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'sensei_app/Register/user_create_complete.html'
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

    liked_notes = all_exam.filter(likes=request.user)


    context={
        'user': login_author,
        'question_list': questions,
        'answer_list': answers,
        'all_questions_num': all_questions_num,
        'all_answers_num': all_answers_num,
        'note_list': liked_notes,
    }

    return render(request, 'sensei_app/UserInfo/user_detail.html', context)

def ActivitiesOfUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    all_questions_num = all_questions.filter(login_author=login_author).count()
    questions = all_questions.filter(login_author=login_author)[:6]

    all_answers = Answer.objects.all()
    all_answers_num = all_answers.filter(login_author=login_author).count()
    answers = all_answers.filter(login_author=login_author)[:6]

    all_exam = jltct.objects.all()

    context = {
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
    template_name = 'sensei_app/UserInfo/Change/user_update.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('sensei_app:user_detail', pk=self.kwargs['pk'])

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('sensei_app:password_change_done')
    template_name = 'sensei_app/UserInfo/Change/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'sensei_app/UserInfo/Change/password_change_done.html'

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'sensei_app/mail_template/password_reset/subject.txt'
    email_template_name = 'sensei_app/mail_template/password_reset/message.txt'
    template_name = 'sensei_app/UserInfo/Change/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('sensei_app:password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'sensei_app/UserInfo/Change/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('sensei_app:password_reset_complete')
    template_name = 'sensei_app/UserInfo/Change/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'sensei_app/UserInfo/Change/password_reset_complete.html'

class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'sensei_app/UserInfo/Change/email_change_form.html'
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
    template_name = 'sensei_app/UserInfo/Change/email_change_done.html'

class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'sensei_app/UserInfo/Change/email_change_complete.html'
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
