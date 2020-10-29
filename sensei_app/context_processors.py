from django.db.models import Count, Q

from sensei_app.models import Question, QuestionCategory, Answer, jltcttag


def common(request):
    context = {
        'question_categories': QuestionCategory.objects.annotate(
            num_posts=Count('question', filter=Q(question__is_public=True))),
        'jltct_tags': jltcttag.objects.annotate(
            num_notes=Count('tag', filter=Q(tags__public=True))),

    }
    return context