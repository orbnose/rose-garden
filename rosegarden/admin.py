from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Branch, Book, BranchUserProfile

class ProfileInline(admin.StackedInline):
    # This calls follows admin  registration recommendations for a user profile per:
    #  https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model

    model = BranchUserProfile
    can_delete = False
    verbose_name_plural = 'branch user profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

#register models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Branch)

admin.site.register(Book)