from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import EmailValidator



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

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.updated_at:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", null=True, blank=True)
    answer = models.ForeignKey('self', on_delete=models.CASCADE, related_name="answer_answer", null=True, blank=True)
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


class Contact(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    email = models.EmailField(null=True, blank=False,)
    content = models.TextField(null=True, blank=False)


