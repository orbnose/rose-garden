from django import forms
from django.forms import Form, ModelForm, Textarea, TextInput

from .models import Book, Branch, BranchUserProfile, author_regex, ddc_regex


# Taken from https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
class BootstrapBaseForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget = visible.field.widget
            if not hasattr(widget, 'input_type'):
                continue
            input_type = widget.input_type
            if input_type == 'text':
                widget.attrs['class'] = 'form-control'
            elif input_type == 'checkbox':
                widget.attrs['class'] = 'form-check'

class BootstrapBaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget = visible.field.widget
            if not hasattr(widget, 'input_type'):
                continue
            input_type = widget.input_type
            if input_type == 'text':
                widget.attrs['class'] = 'form-control'
            elif input_type == 'checkbox':
                widget.attrs['class'] = 'form-check'


class BookForm(BootstrapBaseModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_editor', 'ddc_number', 'version', 'is_biography_or_memoir']
        labels = {
            'author_editor': 'Author or Editor',
            'ddc_number': 'Dewey Decimal Number',
            'is_biography_or_memoir': 'Check if this book is a biography or a memior'
        }
        error_messages = {
            'author_editor': {
                'invalid': "Names must contain alphabetic characters and the following symbols only: . ' -"
            },
            'ddc_number': {
                'invalid': "Dewey Decimal numbers must have 3 digits in from of the decimal place, with at most 12 digits total (e.g. 001 or 321.123456789)"
            },
        }
class UserProfileInterestsForm(BootstrapBaseModelForm):
    class Meta:
        model = BranchUserProfile
        fields = ['interests',]
        widgets = {
            'interests': Textarea,
        }

class QuickSearchForm(BootstrapBaseForm):
    q = forms.CharField(max_length = 200, label='Quick Search')

class FullSearchForm(BootstrapBaseForm):
    f = forms.ChoiceField(
        choices = [
            ('any', 'Any of these filters'),
            ('all', 'All of these filters')],
        label = 'Search Logic'
        )

    title = forms.CharField(required=False, max_length = 200)
    author = forms.CharField(required=False, max_length=60, validators=[author_regex], label="Author or Editor")
    ddcmin = forms.CharField(required=False, max_length=13, validators=[ddc_regex], label="Minimum")
    ddcmax = forms.CharField(required=False, max_length=13, validators=[ddc_regex], label="Maximum")
    cat = forms.ChoiceField(
            required = False,
            label = "Category",
            choices=[
                (None,  '-----------'),
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
    bio = forms.BooleanField(required=False, label="Is the book a biography or memoir?")
    branch = forms.ModelChoiceField(required=False, queryset=Branch.objects.all(), label="Available at Branch")

class DeleteBookForm(Form):
    confirm_delete = forms.BooleanField(initial=True, widget=forms.HiddenInput)