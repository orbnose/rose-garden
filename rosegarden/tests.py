from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings

import html

from http import HTTPStatus

from .models import Book, Branch, BranchUserProfile
from .views import quicksearch_books, fullsearch_books

def setup_and_save_valid_branch(name="Home Branch", location="Madison Wisconsin"):
    branch = Branch(name=name, location=location)
    branch.save()
    return branch

def setup_and_save_valid_book(branch=None, title="The Republic", author="Plato", ddc='312', is_bio=False):
    book = Book(branch=branch, title=title, author_editor=author, ddc_number=ddc, is_biography_or_memoir=is_bio)
    book.save()
    return book

def setup_orphaned_book(title='book1-001-Orphaned Book', author='Orphaned Author', ddc='100'):
    book = Book(branch=None, title=title, author_editor=author, ddc_number=ddc)
    book.save()
    return book

def setup_deleted_book(title='book1-001-Deleted Book', author='Deleted Author', ddc='100', branch=None):
    if branch is None:
        branch = setup_and_save_valid_branch(name='Deleted Branch', location='Nowhere KS')
    book = Book(branch=branch, title=title, author_editor=author, ddc_number=ddc, is_deleted=True)
    book.save()
    return book

def setup_deleted_orphaned_book(title='book1-001-Deleted Orphaned Book', author='Deleted O. Author', ddc='100'):
    book = Book(branch=None, title=title, author_editor=author, ddc_number=ddc, is_deleted=True)
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

def setup_test_book_list():
    branch1 = setup_and_save_valid_branch()
    branch2 = setup_and_save_valid_branch(name="Basement Books", location="Nowhere KS")
    books = [
        setup_and_save_valid_book(branch=branch1, title='book1-001', author='author1-001', ddc='001'),
        setup_and_save_valid_book(branch=branch1, title='book1-101', author='author1-101', ddc='101'),
        setup_and_save_valid_book(branch=branch1, title='book1-201', author='author1-201', ddc='201'),
        setup_and_save_valid_book(branch=branch1, title='book1-301', author='author1-301', ddc='301'),
        setup_and_save_valid_book(branch=branch1, title='book1-401', author='author1-401', ddc='401'),
        setup_and_save_valid_book(branch=branch1, title='book1-501', author='author1-501', ddc='501'),
        setup_and_save_valid_book(branch=branch1, title='book1-601', author='author1-601', ddc='601'),
        setup_and_save_valid_book(branch=branch1, title='book1-701', author='author1-701', ddc='701'),
        setup_and_save_valid_book(branch=branch1, title='book1-801', author='author1-801', ddc='801'),
        setup_and_save_valid_book(branch=branch1, title='book1-901', author='author1-901', ddc='901'),
        setup_and_save_valid_book(branch=branch1, title='book1-bio', author='author1-901', ddc='921', is_bio=True),
        setup_and_save_valid_book(branch=branch2, title='book2-001', author='author1-001', ddc='001'),
        setup_and_save_valid_book(branch=branch2, title='book2-101', author='author1-101', ddc='101'),
        setup_and_save_valid_book(branch=branch2, title='book2-201', author='author1-201', ddc='201'),
        setup_and_save_valid_book(branch=branch2, title='book2-301', author='author1-301', ddc='301'),
        setup_and_save_valid_book(branch=branch2, title='book2-401', author='author1-401', ddc='401'),
        setup_and_save_valid_book(branch=branch2, title='book2-501', author='author1-501', ddc='501'),
        setup_and_save_valid_book(branch=branch2, title='book2-601', author='author1-601', ddc='601'),
        setup_and_save_valid_book(branch=branch2, title='book2-701', author='author1-701', ddc='701'),
        setup_and_save_valid_book(branch=branch2, title='book2-801', author='author1-801', ddc='801'),
        setup_and_save_valid_book(branch=branch2, title='book2-901', author='author2-901', ddc='901'),
        setup_and_save_valid_book(branch=branch2, title='book2-bio', author='author2-901', ddc='921', is_bio=True),
        setup_deleted_book(),
        setup_orphaned_book(),
        setup_deleted_orphaned_book(),
    ]
    return books

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
    

    def test_get_category(self):
        branch = setup_and_save_valid_branch()
        book001 = setup_and_save_valid_book(branch=branch,ddc='001')
        book101 = setup_and_save_valid_book(branch=branch,ddc='101')
        book201 = setup_and_save_valid_book(branch=branch,ddc='201')
        book301 = setup_and_save_valid_book(branch=branch,ddc='301')
        book401 = setup_and_save_valid_book(branch=branch,ddc='401')
        book501 = setup_and_save_valid_book(branch=branch,ddc='501')
        book601 = setup_and_save_valid_book(branch=branch,ddc='601')
        book701 = setup_and_save_valid_book(branch=branch,ddc='701')
        book801 = setup_and_save_valid_book(branch=branch,ddc='801')
        book901 = setup_and_save_valid_book(branch=branch,ddc='901')

        self.assertEquals(book001.get_category(), "Computer science, information and general works")
        self.assertEquals(book101.get_category(), "Philosophy and psychology")
        self.assertEquals(book201.get_category(), "Religion")
        self.assertEquals(book301.get_category(), "Social sciences")
        self.assertEquals(book401.get_category(), "Language")
        self.assertEquals(book501.get_category(), "Science")
        self.assertEquals(book601.get_category(), "Technology")
        self.assertEquals(book701.get_category(), "Arts and recreation")
        self.assertEquals(book801.get_category(), "Literature")
        self.assertEquals(book901.get_category(), "History and geography")

    def test_mark_as_deleted(self):
        book, _ = setup_and_save_valid_book_and_branch()
        pk = book.pk
        book.mark_as_deleted()
        book = None

        book_lookup = Book.objects.get(pk=pk)
        self.assertEquals(book_lookup.branch, None)
        self.assertEquals(book_lookup.is_deleted, True)

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

class BranchUserProfileModelTests(TestCase):
    def test_profile_cannot_edit_book_diff_branch(self):
        book, _ = setup_and_save_valid_book_and_branch()
        profile, _ = setup_valid_profile_and_branch()
        self.assertIs(profile.can_edit_book(book), False)
    
    def test_profile_can_edit_book(self):
        book, branch = setup_and_save_valid_book_and_branch()
        profile, _ = setup_valid_profile_and_user(branch=branch)
        self.assertIs(profile.can_edit_book(book), True)
    
    def test_profile_cannot_edit_book_orphaned(self):
        book = setup_orphaned_book()
        profile, _ = setup_valid_profile_and_branch()
        self.assertIs(profile.can_edit_book(book), False)
    
    def test_profile_cannot_edit_book_deleted(self):
        profile, branch = setup_valid_profile_and_branch()
        book = setup_deleted_book(branch=branch)
        self.assertIs(profile.can_edit_book(book), False)

    def test_profile_cannot_edit_book_deleted_and_orphaned(self):
        book = setup_deleted_orphaned_book()
        profile, _ = setup_valid_profile_and_branch()
        self.assertIs(profile.can_edit_book(book), False)
    
class HomepageTests(TestCase):
    def test_homepage(self):
        _, branch = setup_and_save_valid_book_and_branch()
        _ = setup_and_save_valid_book(branch=branch, title="One Flew Over the Cuckoo's Nest", author="Ken Kesey", ddc=800, is_bio=False)
        setup_deleted_book()
        setup_orphaned_book()
        setup_deleted_orphaned_book()

        response = self.client.get(reverse('rosegarden:index'))
        
        self.assertContains(response, "The Republic")
        self.assertContains(response, html.escape("One Flew Over the Cuckoo's Nest") )
        self.assertNotContains(response, "Deleted Book")
        self.assertNotContains(response, "Orphaned Book")
        self.assertNotContains(response, "Deleted Orphaned Book")

    def test_add_book_link_user_not_authenticated(self):
        response = self.client.get(reverse('rosegarden:index'))
        self.assertNotContains(response, "Add Book")
    
    def test_add_book_link_user_is_authenticated(self):
        _, _ = setup_valid_profile_and_branch()

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:index'))
        self.assertContains(response, "Add Book")

class BookDetailsPageTests(TestCase):
    def test_bookdetails_valid_book(self):
        book, _ = setup_and_save_valid_book_and_branch()
        response = self.client.get(reverse('rosegarden:book_details', args=[book.pk]))
        self.assertContains(response, "The Republic")
        self.assertContains(response, "Plato")
        self.assertContains(response, "312")
    
    def test_bookdetails_orphaned_book(self):
        book = setup_orphaned_book()
        response = self.client.get(reverse('rosegarden:book_details', args=[book.pk]))
        self.assertContains(response, "This book has been removed from the library.")
    
    def test_bookdetails_deleted_book(self):
        book = setup_deleted_book()
        response = self.client.get(reverse('rosegarden:book_details', args=[book.pk]))
        self.assertContains(response, "This book has been removed from the library.")
    
    def test_bookdetails_deleted_book(self):
        book = setup_deleted_book()
        response = self.client.get(reverse('rosegarden:book_details', args=[book.pk]))
        self.assertContains(response, "This book has been removed from the library.")

    def test_bookdetails_user_not_authenticated(self):
        book, _ = setup_and_save_valid_book_and_branch()
        response = self.client.get(reverse('rosegarden:book_details', args=[book.pk]))
        self.assertNotContains(response, "Edit this book")
        self.assertNotContains(response, "Delete this book")

    def test_bookdetails_user_is_authenticated(self):
        book, branch = setup_and_save_valid_book_and_branch()
        setup_valid_profile_and_user(branch=branch)

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:book_details', args=[book.pk]))
        self.assertContains(response, "Edit this book")
        self.assertContains(response, "Delete this book")

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

    @override_settings(CHANGE_PASSWORD_URL=settings.LOGIN_URL)
    def test_userdetails_not_logged_in(self):
        # Don't try changing password in this test - the password change url was set above to 
        #  the same as the login url to ensure something is there even if the project is not
        #  set up to require authentication.

        profile, _ = setup_valid_profile_and_branch()
        username = profile.user.username
        response = self.client.get(reverse('rosegarden:user_details', args=[username]))
        self.assertContains(response, "ben ")
        self.assertContains(response, "Home Branch")
        self.assertContains(response, "sustainable agriculture")
        self.assertNotContains(response, "(Edit)")
        self.assertNotContains(response, "change your password")
        
        password_change_link_piece = '<a href="' + reverse(settings.CHANGE_PASSWORD_URL)
        self.assertNotContains(response, password_change_link_piece)

    @override_settings(CHANGE_PASSWORD_URL=settings.LOGIN_URL)
    def test_userdetails_logged_in_viewing_different_user(self):
        # Don't try changing password in this test - see test_userdetails_not_logged_in

        profile, _ = setup_valid_profile_and_branch()
        username = profile.user.username
        setup_valid_user(username='zaphod',password='pass1')

        if not self.client.login(username="zaphod", password="pass1"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:user_details', args=[username]))
        self.assertContains(response, "ben ")
        self.assertContains(response, "Home Branch")
        self.assertContains(response, "sustainable agriculture")
        self.assertNotContains(response, "(Edit)")
        self.assertNotContains(response, "change your password")

        password_link_piece = '<a href="' + reverse(settings.CHANGE_PASSWORD_URL)
        self.assertNotContains(response, password_link_piece)

        #check that My User Page points to the login user, even when viewing a different user's page
        url = reverse('rosegarden:user_details', args=['zaphod'])
        self.assertContains(response, url+'">My User Page</a>')
    
    def test_userdetails_logged_in_viewing_own_user(self):
        profile, _ = setup_valid_profile_and_branch()
        username = profile.user.username

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:user_details', args=[username]))
        self.assertContains(response, "ben ")
        self.assertContains(response, "Home Branch")
        self.assertContains(response, "sustainable agriculture")
        self.assertContains(response, "(Edit)")
        self.assertContains(response, "change your password")

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

    def test_edit_orphaned_book(self):
        _, branch = setup_valid_profile_and_branch()
        book = setup_orphaned_book()

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')
        
        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 403)
    
    def test_edit_deleted_book(self):
        _, branch = setup_valid_profile_and_branch()
        book = setup_deleted_book(branch=branch)

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')
        
        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 403)
    
    def test_edit_deleted_orphaned_book(self):
        _, branch = setup_valid_profile_and_branch()
        book = setup_deleted_orphaned_book()

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')
        
        response = self.client.get(reverse('rosegarden:edit_book', args=[book.pk]))
        self.assertEquals(response.status_code, 403)

class BookDeletePageTests(TestCase):
    def setUp(self):
        profile, branch = setup_valid_profile_and_branch()
        different_branch = setup_and_save_valid_branch(name="Crazy Cat Library")
        no_branch_user = setup_valid_user(username='nobranch', password='pass')

        #pk 1
        matching_book = setup_and_save_valid_book(branch=branch)
        
        #pk 2
        other_branch_book = setup_and_save_valid_book(branch=different_branch)
        
        #pk 3
        deleted_book = setup_deleted_book(branch=branch)
        
        #pk 4
        orphaned_book = setup_orphaned_book()
        
        #pk 5
        deleted_orphaned_book = setup_deleted_orphaned_book()

    def login(self, username='ben', password='pass'):
        if not self.client.login(username=username, password=password):
            raise ValueError('Test user login failed.')

    def test_delete_book_matching_branch(self):
        delete_url = reverse('rosegarden:delete_book', args=[1])
        details_url = reverse('rosegarden:book_details', args=[1])

        #Navigate to delete page
        self.login()
        response = self.client.get(delete_url)
        self.assertContains(response, "Delete Book")

        #Delete the book
        response = self.client.post(delete_url, data = {'confirm_delete': 'True'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], details_url)
        self.assertEqual(Book.objects.get(pk=1).branch, None)
        self.assertEqual(Book.objects.get(pk=1).is_deleted, True)

        #View details page
        response = self.client.get(details_url)
        self.assertContains(response, "This book has been removed from the library.")

        #Navigate back to delete page
        response = self.client.get(delete_url)
        self.assertEquals(response.status_code, 403)

    def test_delete_book_does_not_exist(self):
        response = self.client.get(reverse('rosegarden:delete_book', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_delete_book_not_authenticated(self):
        response = self.client.get(reverse('rosegarden:delete_book', args=[1]))
        self.assertEquals(response.status_code, 403)
    
    def test_delete_book_not_matching_branch(self):
        self.login()
        response = self.client.get(reverse('rosegarden:delete_book', args=[2]))
        self.assertEquals(response.status_code, 403)

    def test_delete_book_no_user_branch(self):
        self.login(username='nobranch')
        response = self.client.get(reverse('rosegarden:delete_book', args=[1]))
        self.assertEquals(response.status_code, 403)
    
    def test_delete_orphaned_book(self):
        self.login()
        response = self.client.get(reverse('rosegarden:delete_book', args=[4]))
        self.assertEquals(response.status_code, 403)

    def test_delete_deleted_book(self):
        self.login()
        response = self.client.get(reverse('rosegarden:delete_book', args=[3]))
        self.assertEquals(response.status_code, 403)
    
    def test_delete_deleted_orphaned_book(self):
        self.login()
        response = self.client.get(reverse('rosegarden:delete_book', args=[5]))
        self.assertEquals(response.status_code, 403)

class UserDetailsEditPageTests(TestCase):
    def test_edit_userdetails_does_not_exist(self):
        username = 'userdoesnotexist'
        response = self.client.get(reverse('rosegarden:edit_user', args=[username]))
        self.assertEquals(response.status_code, 404)
    
    def test_edit_userdetails_not_authenticated(self):
        profile, _ = setup_valid_profile_and_user()
        username = profile.user.username
        response = self.client.get(reverse('rosegarden:edit_user', args=[username]))
        self.assertEquals(response.status_code, 403)
    
    def test_edit_userdetails_not_matching_user(self):
        
        #creating user ben
        profile, _ = setup_valid_profile_and_user()
        username = profile.user.username

        setup_valid_user(username='zaphod', password='pass1')
        if not self.client.login(username="zaphod", password="pass1"):
            raise ValueError('Test user login failed.')
        
        response = self.client.get(reverse('rosegarden:edit_user', args=[username]))
        self.assertEquals(response.status_code, 403)
    
    def test_edit_userdetails_matching_user(self):
        profile, _ = setup_valid_profile_and_user()
        username = profile.user.username
        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:edit_user', args=[username]))
        self.assertEquals(response.status_code, 200)

class BookAddPageTests(TestCase):
    def test_add_book_user_not_authenticated(self):
        response = self.client.get(reverse('rosegarden:add_book'))
        self.assertEquals(response.status_code, 403)
    
    def test_add_book_user_is_authenticated(self):
        _, _= setup_valid_profile_and_branch()

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        url = reverse('rosegarden:add_book')
        form_html = '<form action="' + url + '" method="post">'
        response = self.client.get(url)
        self.assertContains(response, form_html)

    def test_add_book_user_has_no_branch(self):
        _, _ = setup_valid_profile_and_user()

        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('rosegarden:add_book'))
        self.assertEquals(response.status_code, 403)

class SearchTests(TestCase):
    def setUp(self):
        setup_test_book_list()
    
    def test_fullsearch_or_title_author(self):   
        querydict = {
            'f': 'any',
            'title': 'book1-001',
            'author': 'author1-101',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = ['book1-001','book1-101','book2-101']
        self.assertEquals(target, book_titles)

    def test_fullsearch_or_title_ddcmin(self):
        querydict = {
            'f': 'any',
            'title': 'book1-001',
            'author': '',
            'ddcmin': '800',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = ['book1-001','book1-801','book1-901','book1-bio','book2-801','book2-901','book2-bio']
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_title_ddcmax(self):
        querydict = {
            'f': 'any',
            'title': 'book1-001',
            'author': '',
            'ddcmin': '',
            'ddcmax': '199',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = ['book1-001','book1-101','book2-001','book2-101']
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_title_category(self):
        querydict = {
            'f': 'any',
            'title': 'book1-001',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '400',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = ['book1-001','book1-401','book2-401']
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_title_bio(self):
        querydict = {
            'f': 'any',
            'title': 'book1-001',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': 'True',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = ['book1-001','book1-bio','book2-bio']
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_title_branch(self):
        querydict = {
            'f': 'any',
            'title': 'book1-001',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': Branch.objects.get(pk=2),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = ['book1-001','book2-001','book2-101','book2-201','book2-301','book2-401','book2-501','book2-601','book2-701','book2-801','book2-901','book2-bio']
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_author_ddcmin(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': 'author1-001',
            'ddcmin': '900',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book1-901','book1-bio','book2-901','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_author_ddcmax(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': 'author1-001',
            'ddcmin': '',
            'ddcmax': '200.1',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book1-101','book2-101'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_author_cat(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': 'author1-001',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '300',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book1-301','book2-301'])
        self.assertEquals(target, book_titles)

    def test_fullsearch_or_author_bio(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': 'author1-001',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': 'True',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book1-bio','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_author_branch(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': 'author1-001',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': Branch.objects.get(pk=2),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book2-101','book2-201','book2-301','book2-401','book2-501','book2-601','book2-701','book2-801','book2-901','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_ddcmin_ddcmax(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '199.9',
            'ddcmax': '505.135',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-201','book1-301','book1-401','book1-501','book2-201','book2-301','book2-401','book2-501'])
        self.assertEquals(target, book_titles)

    def test_fullsearch_or_ddcmin_cat(self):
        # Category takes prevelance over DDC range
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '902',
            'ddcmax': '',
            'cat': '800',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-801','book2-801'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_ddcmin_bio(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '899.123123123',
            'ddcmax': '',
            'cat': '',
            'bio': 'True',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-901','book2-901','book1-bio','book2-bio'])
        self.assertEquals(target, book_titles)

    def test_fullsearch_or_ddcmin_branch(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '899.123123123',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': Branch.objects.get(pk=1),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-901','book2-901','book1-bio','book2-bio','book1-001','book1-101','book1-201','book1-301','book1-401','book1-501','book1-601','book1-701','book1-801'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_ddcmax_cat(self):
        # Category search takes prevelance over DDC range
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '002.345',
            'cat': '700',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-701','book2-701'])
        self.assertEquals(target, book_titles)

    def test_fullsearch_or_ddcmax_bio(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '002.345',
            'cat': '',
            'bio': 'True',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book1-bio','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_ddcmax_branch(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '002.345',
            'cat': '',
            'bio': '',
            'branch': Branch.objects.get(pk=2),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-001','book2-001','book2-101','book2-201','book2-301','book2-401','book2-501','book2-601','book2-701','book2-801','book2-901','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_cat_bio(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '200',
            'bio': 'True',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-201','book2-201','book1-bio','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_cat_branch(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '200',
            'bio': '',
            'branch': Branch.objects.get(pk=2),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-201','book2-001','book2-101','book2-201','book2-301','book2-401','book2-501','book2-601','book2-701','book2-801','book2-901','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_or_bio_branch(self):
        querydict = {
            'f': 'any',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': 'True',
            'branch': Branch.objects.get(pk=2),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-bio','book2-001','book2-101','book2-201','book2-301','book2-401','book2-501','book2-601','book2-701','book2-801','book2-901','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_and_title_in_ddcrange(self):
        querydict = {
            'f': 'all',
            'title': 'book1',
            'author': '',
            'ddcmin': '199.8',
            'ddcmax': '400.1',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-201','book1-301'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_and_title_out_ddcrange(self):
        querydict = {
            'f': 'all',
            'title': 'book1-101',
            'author': '',
            'ddcmin': '199.8',
            'ddcmax': '400.1',
            'cat': '',
            'bio': '',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        self.assertEquals([], book_titles)
    
    def test_fullsearch_and_author_bio(self):
        querydict = {
            'f': 'all',
            'title': '',
            'author': 'author1',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': 'True',
            'branch': '',
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_and_author_branch(self):
        querydict = {
            'f': 'all',
            'title': '',
            'author': 'author2',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '',
            'bio': '',
            'branch': Branch.objects.get(pk=2),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book2-901','book2-bio'])
        self.assertEquals(target, book_titles)
    
    def test_fullsearch_and_cat_branch(self):
        querydict = {
            'f': 'all',
            'title': '',
            'author': '',
            'ddcmin': '',
            'ddcmax': '',
            'cat': '900',
            'bio': '',
            'branch': Branch.objects.get(pk=1),
        }
        book_titles = sorted([book.title for book in fullsearch_books(querydict)])
        target = sorted(['book1-901','book1-bio'])
        self.assertEquals(target, book_titles)
    
    def test_quicksearch_page(self):
        query = '?q=book1'
        url = reverse('rosegarden:search') + query
        response = self.client.get(url)
        self.assertContains(response, 'book1-001')
        self.assertContains(response, 'book1-101')
        self.assertContains(response, 'book1-201')
        self.assertContains(response, 'book1-301')
        self.assertContains(response, 'book1-401')
        self.assertContains(response, 'book1-501')
        self.assertContains(response, 'book1-601')
        self.assertContains(response, 'book1-701')
        self.assertContains(response, 'book1-801')
        self.assertContains(response, 'book1-901')
        self.assertContains(response, 'book1-bio')
    
    def test_fullsearch_page(self):
        query = '?f=all&title=book1&cat=000'
        url = reverse('rosegarden:search') + query
        response = self.client.get(url)
        self.assertContains(response, 'book1-001')
        self.assertNotContains(response, 'book1-101')
    
    def test_fullsearch_page_not_found(self):
        query = '?f=any&title=aliens'
        url = reverse('rosegarden:search') + query
        response = self.client.get(url)
        self.assertContains(response, 'No Results Found')