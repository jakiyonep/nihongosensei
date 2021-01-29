from django.db.models import Count, Q

from sensei_app.models import *


def common(request):
    context = {
        'question_categories': QuestionCategory.objects.annotate(
            num_posts=Count('question', filter=Q(question__is_public=True))),
        'note_categories': jltctcategory.objects.annotate(
            num_notes=Count('category', filter=Q(category_notes__public=True))),
        'note_tags': jltcttag.objects.annotate(
            num_notes=Count('tag', filter=Q(tags__public=True))),
        'exp_tags': ExamTags.objects.annotate(
            num_notes=Count('tag', filter=Q(tags__public=True))),
        'material_categories': MaterialCategory.objects.annotate(
            num_materials=Count('category',filter=Q(category_materials__public=True))),
        'material_tags': MaterialTag.objects.annotate(
            num_materials=Count('tag', filter=Q(tag_materials__public=True))),
        'blog_categories': BlogCategory.objects.annotate(
            num_blogs=Count('category', filter=Q(blog_category_posts__public=True))),
        'blog_tags': BlogTag.objects.annotate(
            num_blogs=Count('tag', flter=Q(blog_tag_posts__public=True))),
    }
    return context