from django.urls import path, include
from django.views.generic import TemplateView
from sensei_app.views import *

app_name = 'sensei_app'

urlpatterns =[
    path('', Toppage.as_view(), name='toppage'),
    path('questions/', QuestionList.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name="question_detail"),
    path('question/category/<str:question_category_slug>/', QuestionCategoryView.as_view(), name="question_category"),
    path('question/add/', QuestionAdd, name="question_add"),
    path('question/answer/<int:pk>', AnswerFormView.as_view(), name="answer"),
    path('contact/add', ContactAdd, name='contact_add'),
]

