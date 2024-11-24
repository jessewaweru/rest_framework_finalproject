from rest_framework.test import APITestCase
from rest_framework import status
from schools.models import School


class SchoolViewTest(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School", location="City, County")

    def test_list_schools(self):
        response = self.client.get("/api/schools/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test School")
