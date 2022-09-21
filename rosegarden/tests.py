from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

import html

from .models import Book, Branch

def setup_and_save_valid_branch(name="Home Branch", location="Madison Wisconsin"):
    branch = Branch(name=name, location=location)
    branch.save()
    return branch

def setup_and_save_valid_book(branch=None, title="The Republic", author="Plato", ddc=312, is_bio=False):
    book = Book(branch=branch, title=title, author_editor=author, ddc_number=ddc, is_biography_or_memoir=is_bio)
    book.save()
    return book

def setup_and_save_valid_branch_and_book():
    branch = setup_and_save_valid_branch()
    book = setup_and_save_valid_book(branch=branch)
    return book, branch

class BookModelTests(TestCase):

    
    def test_validator_title_greater_than_200_characters(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.title = "A really long title that is ridiculous for a book. I mean come on, people, would you really even read this far if this were printed on the front of a book displayed front and center of a second-hand type of bookstore?"
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testbook.full_clean()
    
    def test_validator_title_does_not_exist(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.title = ""
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_title_less_than_or_equal_to_200_characters(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.title = "A pithy title"
        testbook.full_clean()
        self.assertTrue( len(testbook.title) <= 200)

    def test_validator_author_greater_than_60_characters(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Smith, Joan Joan Joan Joan Joan Joan-Joan Joanne Joan Joan Joan Joan Joan"
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 60 characters'):
            testbook.full_clean()

    def test_validator_author_less_than_or_equal_to_60_characters(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Smith, Joan Marie"
        testbook.full_clean()
        self.assertTrue( len(testbook.title) <= 60)

    def test_validator_author_does_not_exist(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = ""
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_author_regex1(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Joan Smith"
        testbook.full_clean()

    def test_validator_author_regex2(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "J Smyth"
        testbook.full_clean()

    def test_validator_author_regex3(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Evil Corp Publishing"
        testbook.full_clean()

    def test_validator_author_regex4(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Jules Verne Smith"
        testbook.full_clean()
    
    def test_validator_author_regex5(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Jules-Verne Smith"
        testbook.full_clean()

    def test_validator_author_regex6(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Jules-verne Billy-Joe Smith"
        testbook.full_clean()

    def test_validator_author_regex7(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "a b"
        testbook.full_clean()

    def test_validator_author_regex8(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Plato"
        testbook.full_clean()
    
    def test_validator_author_regex9(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Michael B. Everest-Denali Jordan, Jr."
        testbook.full_clean()
    
    def test_validator_author_regex10(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Miguel d'Argent"
        testbook.full_clean()
    
    def test_validator_author_bad_regex1(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Smith,Joan"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex2(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Smith Joan!"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex3(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Ke$ha Smith"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex4(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = " Joan Smith"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex5(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Joan1 Smoth"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex6(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Joan Smith "
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex7(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Joan- Smith"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex8(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.author_editor = "Joan Smith-"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_is_less_than_zero(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = -1.0001
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_3_digits_before_decimal(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = 1000.1
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_9_digits_after_decimal(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = 312.1234567891
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_bad_numeric_format(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = "312.12345.12"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_alpha_character(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = "312.1a"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_less_than_100_bad(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = 1.1
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_ddc_less_than_100_good(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = "001.1"
        testbook.full_clean()

    def test_validator_ddc_is_valid(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
        testbook.ddc_number = 999.123456789
        testbook.full_clean()
    
    def test_validator_is_biography_not_boolean(self):
        testbook, _ = setup_and_save_valid_branch_and_book()
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
        _, branch = setup_and_save_valid_branch_and_book()
        _ = setup_and_save_valid_book(branch=branch, title="One Flew Over the Cuckoo's Nest", author="Ken Kesey", ddc=800, is_bio=False)

        response = self.client.get(reverse('rosegarden:index'))
        
        self.assertContains(response, "The Republic")
        self.assertContains(response, html.escape("One Flew Over the Cuckoo's Nest") )

class BookDetailsPageTests(TestCase):
    def test_bookdetails(self):
        book, _ = setup_and_save_valid_branch_and_book()
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