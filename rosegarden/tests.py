from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Book

class BookModelTests(TestCase):
    
    def test_validator_title_greater_than_200_characters(self):
        testbook = Book(
            title = "A really long title that is ridiculous for a book. I mean come on, people, would you really even read this far if this were printed on the front of a book displayed front and center of a second-hand type of bookstore?",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 200 characters'):
            testbook.full_clean()
    
    def test_validator_title_does_not_exist(self):
        testbook = Book(
            title = "",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            testbook.full_clean()
    
    def test_validator_title_less_than_or_equal_to_200_characters(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )

    def test_validator_author_greater_than_60_characters(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan Joan Joan Joan Joan Joan Joan Joan Joan Joan Joan Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 60 characters'):
            testbook.full_clean()

    def test_validator_author_less_than_or_equal_to_60_characters(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan Marie",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()
        self.AssertTrue( len(testbook.title) <= 60)

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
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()

    def test_validator_author_regex2(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smyth,J"
        testbook.full_clean()

    def test_validator_author_regex3(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Evil Corp Publishing,"
        testbook.full_clean()

    def test_validator_author_regex4(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smith,Jules Verne"
        testbook.full_clean()
    
    def test_validator_author_regex5(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smith,Jules-Verne"
        testbook.full_clean()

    def test_validator_author_regex6(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smith,Jules-Verne Billy-Joe"
        testbook.full_clean()

    def test_validator_author_bad_regex1(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Plato"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex2(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Sm1th,Kesha"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex3(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smith,Ke$ha"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex4(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smyth, Jules"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex5(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smyth,Jules-"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex6(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smyth,Jules- Verne"
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()
    
    def test_validator_author_bad_regex7(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.author_editor = "Smyth,Jules-Verne "
        with self.assertRaisesMessage(ValidationError, 'Enter a valid value.'):
            testbook.full_clean()