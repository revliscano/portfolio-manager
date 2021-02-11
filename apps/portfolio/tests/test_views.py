from django.test import TestCase, Client
from rest_framework import status

from apps.portfolio.models import Project
from apps.portfolio.serializers import ProjectSerializer
from apps.portfolio.tests.utils import create_three_objects_of


class TestOKCodeForViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_projects_url(self):
        target_url = '/api/projects/'
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetAllProjects(TestCase):
    def setUp(self):
        self.client = Client()
        self.projects = create_three_objects_of(Project)
        self.serialized_projects = ProjectSerializer(self.projects, many=True)

    def test_all_projects_are_returned(self):
        target_url = '/api/projects/'
        response = self.client.get(target_url)
        self.assertEqual(response.data, self.serialized_projects.data)
