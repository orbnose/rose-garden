from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

import html

from .models import Book, Branch, Copy

def setup_and_save_valid_branch(name="Home Branch", location="Madison Wisconsin"):
    branch = Branch(name=name, location=location)
    branch.save()
    return branch

def setup_and_save_valid_book(title="The Republic", author="Plato", ddc=312, is_lit=False, is_bio=False):
    book = Book(title=title, author_editor=author, ddc_number=ddc, is_literature=is_lit, is_biography=is_bio)
    book.save()
    return book

def setup_and_save_valid_copy(branch,book,version=""):
    copy = Copy(branch=branch, book=book, version=version)
    copy.save()
    return copy

def setup_two_copies_of_two_books():
    branch = setup_and_save_valid_branch()

    b1 = setup_and_save_valid_book()
    b2 = setup_and_save_valid_book(title="One Flew Over the Cuckoo's Nest", author="Ken Kesey", ddc=800)

    cpy1 = setup_and_save_valid_copy(branch, b1)
    cpy2 = setup_and_save_valid_copy(branch, b2)

    return cpy1, cpy2

class BookModelTests(TestCase):

    
    def test_validator_title_greater_than_200_characters(self):
        testbook = Book(
            title = "A really long title that is ridiculous for a book. I mean come on, people, would you really even read this far if this were printed on the front of a book displayed front and center of a second-hand type of bookstore?",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testbook.full_clean()
    
    def test_validator_title_does_not_exist(self):
        testbook = Book(
            title = "",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_title_less_than_or_equal_to_200_characters(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
        self.assertTrue( len(testbook.title) <= 200)

    def test_validator_author_greater_than_60_characters(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith, Joan Joan Joan Joan Joan Joan-Joan Joanne Joan Joan Joan Joan Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 60 characters'):
            testbook.full_clean()

    def test_validator_author_less_than_or_equal_to_60_characters(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith, Joan Marie",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
        self.assertTrue( len(testbook.title) <= 60)

    def test_validator_author_does_not_exist(self):
        testbook = Book(
            title = "Cool space stories",
            author_editor = "",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_author_regex1(self):
        #Step 1: Valid Formats
        testbook = Book(
            title = "A pithy title",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_author_regex2(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "J Smyth",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_author_regex3(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Evil Corp Publishing",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_author_regex4(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Jules Verne Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
    
    def test_validator_author_regex5(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Jules-Verne Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_author_regex6(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Jules-verne Billy-Joe Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )

        testbook.full_clean()

    def test_validator_author_regex7(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "a b",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_author_regex8(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
    
    def test_validator_author_regex9(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Michael B. Everest-Denali Jordan, Jr.",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
    
    def test_validator_author_regex10(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Miguel d'Argent",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
    
    def test_validator_author_bad_regex1(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex2(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith Joan!",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex3(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Ke$ha Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex4(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = " Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex5(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Joan1 Smoth",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex6(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Joan Smith ",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex7(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Joan- Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex8(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Joan Smith-",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_is_less_than_zero(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = -1.0001,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_3_digits_before_decimal(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 1000.1,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_9_digits_after_decimal(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 312.1234567891,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_bad_numeric_format(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = "312.12345.12",
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_alpha_character(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = "312.1a",
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_less_than_100_bad(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 1.1,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_less_than_100_good(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = "001.1",
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_ddc_is_valid(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 999.123456789,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
    
    def test_validator_is_literature_not_boolean(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 312.12,
            is_literature = "False flag",
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'value must be either True or False'):
            testbook.full_clean()
    
    def test_validator_is_biography_not_boolean(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 312.12,
            is_literature = False,
            is_biography = "True flag",
            )
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

class CopyModelTests(TestCase):
    def test_validator_valid_copy(self):
        testbook = Book(
            title = "A cool book",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbranch = Branch(name="Home Branch", location="Madison, Wisconsin")
        testcopy = Copy(branch=testbranch, book=testbook)
        self.assertEqual(testcopy.branch.name, "Home Branch")
        self.assertEqual(testcopy.book.title, "A cool book")

    def test_validator_version_too_long(self):
        testbook = Book(
            title = "A cool book",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbranch = Branch(name="Home Branch", location="Madison, Wisconsin")
        testcopy = Copy(
            version = "Old Queen James Edition, by which his honorable majesty the God Emperor has declared a standard for education, decreeing that all children must duly learn from the One True Source, notwithstanding those harsh words of the critics who will most definitely burn come that great judgement day.",
            branch = testbranch,
            book = testbook
            )

        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testcopy.full_clean()
        
    def test_deleted_branch(self):
        testbook = Book(
            title = "A cool book",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.save()

        testbranch = Branch(name="Home Branch", location="Madison, Wisconsin")
        testbranch.save()

        testcopy = Copy(version="The old one", branch=testbranch, book=testbook)
        testcopy.save()
        pk = testcopy.pk

        testbranch.delete()
        
        reloadedcopy = Copy.objects.get(pk=pk)
        self.assertEqual(reloadedcopy.branch, None)
    
    def test_deleted_book(self):
        testbook = Book(
            title = "A mediocre book",
            author_editor = "Joan Smith",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.save()

        testbranch = Branch(name="Home Branch", location="Madison, Wisconsin")
        testbranch.save()

        testcopy = Copy(version="The old one", branch=testbranch, book=testbook)
        testcopy.save()
        pk = testcopy.pk
        testbook.delete()

        with self.assertRaises(Copy.DoesNotExist):
            Copy.objects.get(pk=pk)

class HomepageTests(TestCase):
    def test_homepage(self):
        _,_=setup_two_copies_of_two_books()

        response = self.client.get(reverse('rosegarden:index'))
        
        self.assertContains(response, "The Republic")
        self.assertContains(response, html.escape("One Flew Over the Cuckoo's Nest") )

class BookDetailsPageTests(TestCase):
    def test_bookdetails(self):
        copy1, _ = setup_two_copies_of_two_books()
        pk = copy1.pk
        response = self.client.get(reverse('rosegarden:book_details', args=[pk]))
        self.assertContains(response, "The Republic")
        self.assertContains(response, "Plato")
        self.assertContains(response, "312")