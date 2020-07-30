from django.db.models import Count, Q

from sensei_app.models import Question, QuestionCategory


def common(request):
    context = {
        'question_categories': QuestionCategory.objects.annotate(
            num_posts=Count('question', filter=Q(question__is_public=True))),
    }
    return context