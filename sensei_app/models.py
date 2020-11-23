from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import EmailValidator

from markdownx.models import MarkdownxField


# USER REGISTRATION

class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('メールアドレス'), unique=True)
    nickname = models.CharField(_('ニックネーム'), max_length=150, blank=True, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email

# Question

class QuestionCategory(models.Model):
    category_name = models.CharField(null=True, blank=False, max_length=100)
    category_slug = models.CharField(null=True, blank=False, max_length=100)

    def __str__(self):
        return self.category_name

class Question(models.Model):
    title = models.CharField(null=True, blank=False, max_length=150)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, null=True, blank=False)
    author = models.CharField(null=True, blank=True, max_length=50)
    login_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_author', null=True, blank=True)
    content = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='test_images', null=True, blank=True)
    addition = models.TextField(null=True, blank=True)
    poll_question = models.TextField(null=True, blank=True)
    option_1 = models.CharField(null=True, blank=True, max_length=100)
    option_2 = models.CharField(null=True, blank=True, max_length=100)
    option_3 = models.CharField(null=True, blank=True, max_length=100)
    option_4 = models.CharField(null=True, blank=True, max_length=100)
    answered_user = models.ManyToManyField(User, null=True, blank=True, related_name="answered_polls")
    option_1_count = models.IntegerField(default=0)
    option_2_count = models.IntegerField(default=0)
    option_3_count = models.IntegerField(default=0)
    option_4_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created_at']

    def answer_reply_num(self):
        answer_num = self.answers.count()
        reply_num = 0
        for answer in self.answers.all():
            reply_num = reply_num + answer.replies.count()
        total = answer_num + reply_num

        return total

    def save(self, *args, **kwargs):
        if self.is_public and not self.updated_at:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def poll_result(self):
        context={}
        option_1_count = self.option_1_count
        option_2_count = self.option_2_count
        option_3_count = self.option_3_count
        option_4_count = self.option_4_count
        count_dict = [option_1_count, option_2_count, option_3_count, option_4_count]
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

        return context

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", null=True, blank=True)
    author = models.CharField(null=True, blank=True, max_length=50)
    login_author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_author_answer', null=True, blank=True )
    content = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        sliced_content = self.content[:10]
        return sliced_content
    class Meta:
        ordering=['-created_at']

class Reply(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    author = models.CharField(null=True, blank=True, max_length=50)
    login_author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_author_reply', null=True, blank=True )
    content = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        sliced_content = self.content[:10]
        return sliced_content
    class Meta:
        ordering=['-created_at']

# Contact

class Contact(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    email = models.EmailField(null=True, blank=False,)
    content = models.TextField(null=True, blank=False)

# JLTCT

class jltctsection(models.Model):
    section = models.CharField(null=False, blank=False, max_length=200)
    section_slug = models.CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        return self.section

class jltcttag(models.Model):
    tag = models.CharField(null=False, blank=False, max_length=200)
    tag_slug = models.CharField(null=False, blank=False, max_length=200, unique=True)

    def __str__(self):
        return self.tag

class jltct(models.Model):
    title = models.CharField(null=False, blank=False, max_length=200)
    title_slug = models.CharField(null=False, blank=False, max_length=200, unique=True)
    number = models.IntegerField(null=True, blank=True)
    section = models.ForeignKey(jltctsection, on_delete=models.CASCADE, related_name="section_name", blank=False, null=True)
    tag = models.ManyToManyField(jltcttag, related_name="tags", blank=True, null=True)
    content = MarkdownxField(null=False, blank=False)
    public = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to="JLTCT_thumbnail", null=True, blank=True)
    related_note = models.ManyToManyField('self', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['section','number']

class jltctreference(models.Model):
    note = models.ForeignKey(jltct,on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)

class Exam(models.Model):
    year = models.IntegerField(null=True, blank=True)
    section = models.IntegerField(null=True, blank=True)
    question_num = models.IntegerField(null=True, blank=True)
    question_head = models.CharField(null=True, blank=True, max_length=200)
    explanation = models.TextField(null=True, blank=True)

    class Answer(models.IntegerChoices):
        choice1 = 1
        choice2 = 2
        choice3 = 3
        choice4 = 4
        choice5 = 5

    answer = models.IntegerField(choices=Answer.choices, null=True)

    updated = models.DateTimeField(auto_now=True)

# Others

class MarkdownExpModel(models.Model):
    htmltag = models.CharField(null=True, blank=True, max_length=100)
    exp = models.TextField(null=True, blank=True)
    before = models.TextField(null=True, blank=True)
    after = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.htmltag

class RegisterPerk(models.Model):
    perk = models.CharField(null=True, blank=True, max_length=100)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.perk

class TermsConditions(models.Model):
    number = models.IntegerField(null=False, blank=True, default=0)
    content = models.TextField(null=False, blank=False)
    create_at = models.DateField(auto_created=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.number)