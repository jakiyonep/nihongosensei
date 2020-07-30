from django.db import models
from django.utils import timezone

class QuestionCategory(models.Model):
    category_name = models.CharField(null=True, blank=False, max_length=100)
    category_slug = models.CharField(null=True, blank=False, max_length=100)

    def __str__(self):
        return self.category_name

class Question(models.Model):
    title = models.CharField(null=True, blank=False, max_length=150)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, null=True, blank=False)
    author = models.CharField(null=True, blank=False, max_length=50)
    content = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='test_images', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.updated_at:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.CharField(null=True, blank=False, max_length=50)
    content = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        sliced_content = self.content[:10]
        return sliced_content