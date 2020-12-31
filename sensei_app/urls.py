from django.urls import path, include
from django.views.generic import TemplateView
from sensei_app.views import *
from . import views

app_name = 'sensei_app'

urlpatterns =[
    path('', Toppage.as_view(), name='toppage'),

    path('sitedesc/', SiteDescView, name="site_desc"),

    path('questions/', QuestionList, name='question_list'),
    path('question/<int:pk>/', QuestionDetail, name="question_detail"),
    path('question/category/<str:question_category_slug>/', QuestionCategoryView, name="question_category"),
    path('question/add/', QuestionAdd, name="question_add"),
    path('question/addition/', QuestionAddition, name="question_addition"),
    path('question/pollvote/', QuestionPollVote, name="question_vote_poll"),
    path('question/answer', AnswerAdd, name="answer_add"),
    path('question/answer/like', views.AnswerLike, name="answer_like"),
    path('question/reply', ReplyAdd, name="reply_add"),
    path('question/delete/<int:pk>/', QuestionDelete, name="question_delete"),
    path('question/answer/delete/<int:pk>', AnswerDelete, name="answer_delete"),
    path('question/reply/delete/<int:pk>', ReplyDelete, name="reply_delete"),

    path('contact/add', ContactAdd, name='contact_add'),

    path('markdownexp/', Markdown_Exp, name='markdownexp'),

    path('termsandconditions/', TermsConditionsView, name="termsandconditions"),
    path('privacypolicy/', PrivacyPolicyView, name="privacypolicy"),

    path('jltct', JLTCTTop, name='jltct_top'),
    path('jltct/tag/<str:tag_slug>', JLTCTTagNotes, name="tag_notes"),
    path('jltct/category/<str:category_slug>', JLTCTCategoryNotes, name="category_notes"),
    path('jltct/note/<str:title_slug>', JLTCTNoteDetail, name="note_detail"),
    path('jltct/exp/<int:year>/<int:section>/<int:question_num>', ExamExpDetail, name="exp_detail"),
    path('jltct/exp/tag/<str:tag_slug>', ExamTagList, name="exp_tag_list"),
    path('jltct/like', views.NoteLike, name="note_like"),
    path('jltct/comment', JltctCommentAdd, name="jltct_comment_add"),
    path('jltct/reply', JltctReplyAdd, name="jltct_reply_add"),
    path('jltct/comment/delete/<int:pk>',JltctCommentDelete, name="note_comment_delete" ),
    path('jltct/reply/delete/<int:pk>',JltctReplyDelete, name='note_reply_delete' ),

    path('material/', MaterialTop, name='material_top'),
    path('material/category/<str:category_slug>', MaterialCategoryList, name="material_category_list"),
    path('material/tag/<str:tag_slug>', MaterialTagList, name="material_tag_list"),
    path('material/upload', MaterialUpload.as_view(), name='material_upload'),

    path('blog', BlogTop, name="blog_top"),
    path('blog/<int:pk>', BlogDetail, name="blog_detail"),
    path('blog/category/<str:category_slug>', BlogCategoryList, name="blog_category_list"),
    path('blog/tag/<str:tag_slug>', BlogTagList, name="blog_tag_list"),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('register/perk/', RegisterPerkList, name="register_perk"),

    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail, name='user_detail'),
    path('user_detail/<int:pk>/questions', AllQuestionsofUser, name="all_questions_of_user"),
    path('user_detail/<int:pk>/answers', AllAnswersofUser, name='all_answers_of_user'),
    path('user_detail/<int:pk>/activities', ActivitiesOfUser, name='activities_of_user'),
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

