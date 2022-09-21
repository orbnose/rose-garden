from django.db import models
from django.core import validators

author_regex = validators.RegexValidator(regex=r"^[A-z]+(([,.] |[ '-])[A-z]+)*(\.?)( [IVXLCDM]+)?$")
# Slightly modified version of Aman Godara's choice 3 from https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name
# Author name should be in the format First Middle1 Middle2 Last
# Allow for alphabetic, comma, - and ' characters only in the author or editor name.

ddc_regex = validators.RegexValidator(regex=r"^\d{3}(\.{1}\d{1,9})?$")

class Branch(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

class Book(models.Model):
    branch = models.ForeignKey(to=Branch, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    author_editor = models.CharField(max_length=60, validators=[author_regex])
    ddc_number = models.CharField(max_length=13, validators=[ddc_regex])
    version = models.CharField(max_length=200, blank=True)
    is_biography_or_memoir = models.BooleanField()