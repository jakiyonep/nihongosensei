from django.urls import path, include
from django.views.generic import TemplateView
from sensei_app.views import *
from . import views

app_name = 'sensei_app'

urlpatterns =[
    path('', Toppage.as_view(), name='toppage'),
    path('questions/', QuestionList.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name="question_detail"),
    path('question/category/<str:question_category_slug>/', QuestionCategoryView.as_view(), name="question_category"),
    path('question/add/', QuestionAdd, name="question_add"),
    path('question/answer/<int:pk>', AnswerAdd, name="answer"),
    path('question/reply/<int:pk>', ReplyAdd, name='reply'),
    path('contact/add', ContactAdd, name='contact_add'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail, name='user_detail'),
    path('user_detail/<int:pk>/questions', AllQuestionsofUser, name="all_questions_of_user"),
    path('user_detail/<int:pk>/answers', AllAnswersofUser, name='all_answers_of_user'),
    path('user_detail/<int:pk>/question_list', ActivitiesOfUser, name='activities_of_user'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
]

