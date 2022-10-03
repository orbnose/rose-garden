from django.db import models
from django.conf import settings
from django.core import validators

author_regex = validators.RegexValidator(regex=r"^[A-z]+(([,.] |[ '-])[A-z]+)*(\.?)( [IVXLCDM]+)?$")
# Slightly modified version of Aman Godara's choice 3 from https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name
# Author name should be in the format First Middle1 Middle2 Last
# Allow for alphabetic, comma, - and ' characters only in the author or editor name.

ddc_regex = validators.RegexValidator(regex=r"^\d{3}(\.{1}\d{1,9})?$")

class Branch(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    branch = models.ForeignKey(to=Branch, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    author_editor = models.CharField(max_length=60, validators=[author_regex])
    ddc_number = models.CharField(max_length=13, validators=[ddc_regex])
    version = models.CharField(max_length=200, blank=True)
    is_biography_or_memoir = models.BooleanField()

    verbose_name_plural = 'books'
    
    def __str__(self):
        return self.title

    def get_category(self):
        
        #Keep only the hundreds place
        ddc= int(float(self.ddc_number)/100)*100

        categories = {
            0:   'Computer science, information and general works',
            100: 'Philosophy and psychology',
            200: 'Religion',
            300: 'Social sciences',
            400: 'Language',
            500: 'Science',
            600: 'Technology',
            700: 'Arts and recreation',
            800: 'Literature',
            900: 'History and geography',
        }
        
        try:
            cat = categories[ddc]
        except KeyError:
            return None

        return cat

class BranchUserProfile(models.Model):
    # This class is setup to track user settings specific to the rose garden app
    #  that are extensions of the base user class currently used for authentication
    #  by the current project. This class uses recommendations per: 
    #  https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.SET_NULL, null=True)
    interests = models.CharField(max_length=500, blank=True, null=True)

    def can_edit_book(self, book):
        if not book:
            return False
        
        if not (self.branch.pk == book.branch.pk):
            return False
        
        return True
    
    def matches_request_user(self, request):
        #Return True if the request user matches the user with this profile. Otherwise False.
        return (request.user.username == self.user.username)