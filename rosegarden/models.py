from django.db import models
from django.core import validators

author_regex = validators.RegexValidator(regex='^[A-z]+(-?[A-z]+)?,({1}([A-z]+(-?[A-z]+)?)?( ?[A-z]+)?)?$')
# Author name should be in the format Lastname,Firstname[ ][MiddleName1][ ][MiddleName2]
# Allow for alphabetic, commas, and hyphen characters only in the author or editor name. Only 1 comma in the middle allowed.
# Hyphens allowed between alphabetic characters, and spaces allowed between firstname alphabetic characters.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author_editor = models.CharField(max_length=60, validators=[author_regex])
    ddc_number = models.DecimalField(max_digits=12, decimal_places=9)
    is_literature = models.BooleanField()
    is_biography = models.BooleanField()