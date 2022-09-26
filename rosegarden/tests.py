from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import html

from .models import Book, Branch, BranchUserProfile

def setup_and_save_valid_branch(name="Home Branch", location="Madison Wisconsin"):
    branch = Branch(name=name, location=location)
    branch.save()
    return branch

def setup_and_save_valid_book(branch=None, title="The Republic", author="Plato", ddc=312, is_bio=False):
    book = Book(branch=branch, title=title, author_editor=author, ddc_number=ddc, is_biography_or_memoir=is_bio)
    book.save()
    return book

def setup_and_save_valid_book_and_branch():
    branch = setup_and_save_valid_branch()
    book = setup_and_save_valid_book(branch=branch)
    return book, branch

def setup_valid_user(username="ben",password="pass"):
    user = User.objects.create_user(username=username, password=password)
    return user

def setup_and_save_profile(user=None, branch=None, interests=None):
    profile = BranchUserProfile(user=user, branch=branch, interests=interests)
    profile.save()
    return profile

def setup_valid_profile_and_user(branch=None, interests=None):
    user = setup_valid_user()
    profile = setup_and_save_profile(user=user, branch=branch, interests=interests)
    return profile, user

def setup_valid_profile_and_branch():
    branch = setup_and_save_valid_branch()
    user = setup_valid_user()
    profile = setup_and_save_profile(user=user, branch=branch, interests='sustainable agriculture')
    return profile, branch

class BookModelTests(TestCase):

    
    def test_validator_title_greater_than_200_characters(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.title = "A really long title that is ridiculous for a book. I mean come on, people, would you really even read this far if this were printed on the front of a book displayed front and center of a second-hand type of bookstore?"
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testbook.full_clean()
    
    def test_validator_title_does_not_exist(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.title = ""
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_title_less_than_or_equal_to_200_characters(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.title = "A pithy title"
        testbook.full_clean()
        self.assertTrue( len(testbook.title) <= 200)

    def test_validator_author_greater_than_60_characters(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Smith, Joan Joan Joan Joan Joan Joan-Joan Joanne Joan Joan Joan Joan Joan"
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 60 characters'):
            testbook.full_clean()

    def test_validator_author_less_than_or_equal_to_60_characters(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Smith, Joan Marie"
        testbook.full_clean()
        self.assertTrue( len(testbook.title) <= 60)

    def test_validator_author_does_not_exist(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = ""
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_author_regex1(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Joan Smith"
        testbook.full_clean()

    def test_validator_author_regex2(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "J Smyth"
        testbook.full_clean()

    def test_validator_author_regex3(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Evil Corp Publishing"
        testbook.full_clean()

    def test_validator_author_regex4(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Jules Verne Smith"
        testbook.full_clean()
    
    def test_validator_author_regex5(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Jules-Verne Smith"
        testbook.full_clean()

    def test_validator_author_regex6(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Jules-verne Billy-Joe Smith"
        testbook.full_clean()

    def test_validator_author_regex7(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "a b"
        testbook.full_clean()

    def test_validator_author_regex8(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Plato"
        testbook.full_clean()
    
    def test_validator_author_regex9(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Michael B. Everest-Denali Jordan, Jr."
        testbook.full_clean()
    
    def test_validator_author_regex10(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Miguel d'Argent"
        testbook.full_clean()
    
    def test_validator_author_bad_regex1(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Smith,Joan"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex2(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Smith Joan!"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex3(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Ke$ha Smith"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex4(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = " Joan Smith"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex5(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Joan1 Smoth"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex6(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Joan Smith "
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex7(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Joan- Smith"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex8(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.author_editor = "Joan Smith-"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_is_less_than_zero(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = -1.0001
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_3_digits_before_decimal(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = 1000.1
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_9_digits_after_decimal(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = 312.1234567891
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_bad_numeric_format(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = "312.12345.12"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_alpha_character(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = "312.1a"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_less_than_100_bad(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = 1.1
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_less_than_100_good(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = "001.1"
        testbook.full_clean()

    def test_validator_ddc_is_valid(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.ddc_number = 999.123456789
        testbook.full_clean()
    
    def test_validator_is_biography_not_boolean(self):
        testbook, _ = setup_and_save_valid_book_and_branch()
        testbook.is_biography_or_memoir = "True flag"

        with self.assertRaisesMessage(ValidationError, 'value must be either True or False'):
            testbook.full_clean()

class BranchModelTests(TestCase):
    def test_validator_valid_branch(self):
        testbranch = Branch(name="Home Branch", location="Madison WI")
    
    def test_validator_name_too_long(self):
        testbranch = Branch(name="Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch Home Branch", location="Madison WI")
        
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testbranch.full_clean()
    
    def test_validator_location_too_long(self):
        testbranch = Branch(name="Home Branch", location="Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison-Madisonshmadison, Wisconsin")
        
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testbranch.full_clean()

class HomepageTests(TestCase):
    def test_homepage(self):
        _, branch = setup_and_save_valid_book_and_branch()
        _ = setup_and_save_valid_book(branch=branch, title="One Flew Over the Cuckoo's Nest", author="Ken Kesey", ddc=800, is_bio=False)

        response = self.client.get(reverse('rosegarden:index'))
        
        self.assertContains(response, "The Republic")
        self.assertContains(response, html.escape("One Flew Over the Cuckoo's Nest") )

class BookDetailsPageTests(TestCase):
    def test_bookdetails(self):
        book, _ = setup_and_save_valid_book_and_branch()
        pk = book.pk
        response = self.client.get(reverse('rosegarden:book_details', args=[pk]))
        self.assertContains(response, "The Republic")
        self.assertContains(response, "Plato")
        self.assertContains(response, "312")

class BranchDetailsPageTests(TestCase):
    def test_branchdetails(self):
        branch = setup_and_save_valid_branch()
        pk = branch.pk
        response = self.client.get(reverse('rosegarden:branch_details', args=[pk]))
        self.assertContains(response, "Name:")
        self.assertContains(response, "Location:")
        self.assertContains(response, "Branch Users:")
        self.assertContains(response, "Home Branch")
        self.assertContains(response, "Madison Wisconsin")

class BranchListPageTests(TestCase):
    def test_branchlist(self):
        _ = setup_and_save_valid_branch()
        response = self.client.get(reverse('rosegarden:branch_list'))
        self.assertContains(response, "Home Branch")
        self.assertContains(response, "Madison Wisconsin")

class UserListPageTests(TestCase):
    def test_userlist(self):
        _, _ = setup_valid_profile_and_branch()
        response = self.client.get(reverse('rosegarden:user_list'))
        self.assertContains(response, 'ben')
        self.assertContains(response, 'Home Branch')

    def test_userlist_user_without_profile(self):
        _ = setup_and_save_valid_branch()
        _ = setup_valid_user(username='bob123')
        response = self.client.get(reverse('rosegarden:user_list'))
        self.assertNotContains(response, 'bob123')

class UserDetailPageTests(TestCase):
    def test_userdetails(self):
        profile, _ = setup_valid_profile_and_branch()
        username = profile.user.username
        response = self.client.get(reverse('rosegarden:user_details', args=[username]))
        self.assertContains(response, "ben ")
        self.assertContains(response, "Home Branch")
        self.assertContains(response, "sustainable agriculture")

class BookEditPageTests(TestCase):
    def test_edit_book_does_not_exist(self):
        response = self.client.get(reverse('rosegarden:edit_book', args=[1]))
        self.assertEquals(response.status_code, 404)
    
    def test_edit_book_not_authenticated(self):
        book, _ = setup_and_save_valid_book_and_branch()
        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 403)
    
    def test_edit_book_not_matching_branch(self):
        book, _ = setup_and_save_valid_book_and_branch()
        branch2 = setup_and_save_valid_branch("Ben's Branch", "Nowhere KS")
        _, _ = setup_valid_profile_and_user(branch=branch2, interests='farming')
        
        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 403)
    
    def test_edit_book_matching_branch(self):
        _, branch = setup_valid_profile_and_branch()
        book = setup_and_save_valid_book(branch=branch)

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 200)
    
    def test_edit_book_no_user_branch(self):
        book, _ = setup_and_save_valid_book_and_branch()
        _ = setup_valid_user()

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 403)