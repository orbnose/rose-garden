from django import forms
from django.forms import Form, ModelForm, Textarea

from .models import Book, Branch, BranchUserProfile, author_regex, ddc_regex

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

class QuickSearchForm(Form):
    pass

class FullSearchForm(Form):
    logic = forms.ChoiceField(choices=[
        ('any', 'Any of these filters'),
        ('all', 'All of these filters')])

    title = forms.CharField(required=False, max_length = 200)
    author_editor = forms.CharField(required=False, max_length=60, validators=[author_regex])
    ddc_lower = forms.CharField(required=False, max_length=13, validators=[ddc_regex])
    ddc_upper = forms.CharField(required=False, max_length=13, validators=[ddc_regex])
    ddc_category = forms.ChoiceField(required=False, choices=[
        ('000', 'Computer science, information & general works'),
        ('100', 'Philosophy & psychology'),
        ('200', 'Religion'),
        ('300', 'Social sciences'),
        ('400', 'Language'),
        ('500', 'Science'),
        ('600', 'Technology'),
        ('700', 'Arts & recreation'),
        ('800', 'Literature'),
        ('900', 'History & geography'),])
    is_biography_or_memoir = forms.BooleanField(required=False)
    available_at_branch = forms.ModelChoiceField(required=False, queryset=Branch.objects.all())