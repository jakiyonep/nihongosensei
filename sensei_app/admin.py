from django.contrib import admin
from sensei_app.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from markdownx.admin import MarkdownxModelAdmin
from .models import User



class jltctReferences(admin.TabularInline):
    model = jltctreference
    extra = 1

class jltctAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'number', 'public')
    list_editable = ['number']
    inlines = [
        jltctReferences
    ]



# USER REGISTRATION

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ['nickname']}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'nickname', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'nickname')
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)

admin.site.register(Contact)
admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)

admin.site.register(Exam)
admin.site.register(jltct,jltctAdmin)
admin.site.register(jltcttag)
admin.site.register(jltctsection)

admin.site.register(MarkdownExpModel)
admin.site.register(RegisterPerk)
admin.site.register(TermsConditions)