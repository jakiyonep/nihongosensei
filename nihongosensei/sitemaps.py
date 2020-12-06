from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.shortcuts import resolve_url


from sensei_app.models import *


class QuestionSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Question.objects.all()

    # モデルに get_absolute_url() が定義されている場合は不要
    def location(self, obj):
        return resolve_url('sensei_app:question_detail', pk=obj.pk)

    def lastmod(self, obj):
        return obj.created_at

class JltctNoteSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.8

    def items(self):
        return jltct.objects.all()

    # モデルに get_absolute_url() が定義されている場合は不要
    def location(self, obj):
        return resolve_url('sensei_app:note_detail', title_slug=obj.title_slug)

    def lastmod(self, obj):
        return obj.update

class ExamSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.8

    def items(self):
        return ExamExp.objects.all()

    # モデルに get_absolute_url() が定義されている場合は不要
    def location(self, obj):
        return resolve_url('sensei_app:exp_detail', year=obj.year, section=obj.section, question_num=obj.question_num)

    def lastmod(self, obj):
        return obj.updated

class UserSitemap(Sitemap):
    """
    静的ページのサイトマップ
    """
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return User.objects.all()

    def location(self, obj):
        return resolve_url('sensei_app:user_detail', pk=obj.pk)


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [
            'sensei_app:toppage',
            'sensei_app:question_list',
            'sensei_app:question_add',
            'sensei_app:contact_add',
            'sensei_app:login',
            'sensei_app:logout',
            'sensei_app:user_create',
            'sensei_app:user_create_done',

        ]
    def location(self, obj):
        return resolve_url(obj)
