from django.forms import ModelForm, Textarea

from .models import Book, BranchUserProfile

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_editor', 'ddc_number', 'version', 'is_biography_or_memoir']

class UserProfileInterestsForm(ModelForm):
    class Meta:
        model = BranchUserProfile
        fields = ['interests',]
        widgets = {
            'interests': Textarea(),
        }