from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Branch, Book, BranchUserProfile

class ProfileInline(admin.StackedInline):
    # This calls follows admin registration recommendations for a user profile per:
    #  https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model

    model = BranchUserProfile
    can_delete = False
    verbose_name_plural = 'branch user profile'

# Use django-import-export if it is installed
try:
    from import_export.admin import ImportExportMixin, ImportExportModelAdmin
    from import_export.resources import ModelResource
    
    using_import_export = True

    class BranchResource(ModelResource):
        class Meta:
            model = Branch
            clean_model_instances = True
    
    class BookResource(ModelResource):
        class Meta:
            model = Book
            clean_model_instances = True
    
    class ProfileResource(ModelResource):
        class Meta:
            model = BranchUserProfile
            clean_model_instances = True
    
    class UserAdmin(ImportExportMixin, BaseUserAdmin):
        inlines = (ProfileInline,)
        class Meta:
            clean_model_instances = True
except ImportError:
    ImportExportModelAdmin = ModelAdmin
    using_import_export = False
    class UserAdmin(BaseUserAdmin):
        inlines = (ProfileInline,)

class BranchAdmin(ImportExportModelAdmin):
    if using_import_export:
        resource_class = BranchResource

class BookAdmin(ImportExportModelAdmin):
    if using_import_export:
        resource_class = BookResource

class ProfileAdmin(ImportExportModelAdmin):
    if using_import_export:
        resource_class = ProfileResource

#register models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Branch, BranchAdmin)

admin.site.register(Book, BookAdmin)

admin.site.register(BranchUserProfile, ProfileAdmin)