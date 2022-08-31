from django.test import TestCase

from .models import Book

class BookModelTests(TestCase):
    
    def test_validator_title_greater_than_200_characters():
        testbook = Book(
            title = "A really long title that is ridiculous for a book. I mean come on, people, would you really even read this far if this were printed on the front of a book displayed front and center of a second-hand type of bookstore?",
            author_editor = "Smith,Joan",
            ddc_number = 400,
            is_literature = False,
            is_biography = False,
            )
        testbook.full_clean()