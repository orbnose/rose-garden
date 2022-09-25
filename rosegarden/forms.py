from django.forms import ModelForm

from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_editor', 'ddc_number', 'version', 'is_biography_or_memoir']
