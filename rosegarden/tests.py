from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Book

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
        with self.assertRaisesMessage(ValidationError, 'Ensure this value is greater than or equal to 0.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_3_digits_before_decimal(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 1000.1,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Ensure that there are no more than 3 digits before the decimal point.'):
            testbook.full_clean()
    
    def test_validator_ddc_more_than_9_digits_after_decimal(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 312.12345678910,
            is_literature = False,
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'Ensure that there are no more than 9 digits after the decimal point.'):
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
            ddc_number = 312.12345678910,
            is_literature = "False",
            is_biography = False,
            )
        with self.assertRaisesMessage(ValidationError, 'value must be either True or False'):
            testbook.full_clean()
    
    def test_validator_is_biography_not_boolean(self):
        testbook = Book(
            title = "A pithy title",
            author_editor = "Plato",
            ddc_number = 312.12345678910,
            is_literature = False,
            is_biography = "True",
            )
        with self.assertRaisesMessage(ValidationError, 'value must be either True or False'):
            testbook.full_clean()