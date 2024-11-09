# from django.test import TestCase
# from users.models import User
# from schools.models import School
# from users.models import Review


# class UserModelTest(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(
#             username="testuser", password="password123", is_school=False
#         )

#     def test_user_creation(self):
#         """Test if a user instance is created successfully."""
#         self.assertIsInstance(self.user, User)
#         self.assertEqual(self.user.username, "testuser")

#     def test_password_is_hashed(self):
#         """Test that the user's password is stored as a hash, not plaintext."""
#         self.assertNotEqual(self.user.password, "password123")
#         self.assertTrue(self.user.check_password("password123"))

#     def test_get_school_profile_none(self):
#         """Test that get_school_profile returns None if no school profile is associated."""
#         self.assertIsNone(self.user.get_school_profile())


# class ReviewModelTest(TestCase):
#     def setUp(self):
#         # Create test user and school
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )
#         self.school = School.objects.create(name="Test School")

#     def test_review_creation(self):
#         """Test if a review can be created for a school by a user."""
#         review = Review.objects.create(
#             user=self.user, school=self.school, comment="Great school!", rating=4
#         )
#         self.assertEqual(review.user, self.user)
#         self.assertEqual(review.school, self.school)
#         self.assertEqual(review.comment, "Great school!")
#         self.assertEqual(review.rating, 4)
