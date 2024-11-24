from django.test import TestCase
from schools.models import School


class SchoolModelTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(
            name="Test School",
            location="City, County",
            rating=4.5,
        )

    def test_school_creation(self):
        self.assertEqual(self.school.name, "Test School")
        self.assertEqual(str(self.school), "Test School")  # Check __str__ method
