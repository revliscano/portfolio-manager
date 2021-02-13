from django.test import TestCase, Client
from rest_framework import status

from apps.portfolio.models import Project
from apps.portfolio.serializers import (
    ProjectSerializer,
    ProjectPreviewSerializer
)
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
        self.target_url = '/api/projects/'

    def test_all_projects_are_returned(self):
        serialized_projects = ProjectSerializer(self.projects, many=True)
        response = self.client.get(self.target_url)
        self.assertEqual(response.data, serialized_projects.data)

    def test_all_projects_with_preview_queryparam(self):
        serialized_projects_for_preview = ProjectPreviewSerializer(
            self.projects,
            many=True
        )
        serialized_projects_full = ProjectSerializer(
            self.projects,
            many=True
        )

        self.performRequests()

        self.assertResponsesWithPreviewReturn(serialized_projects_for_preview)
        self.assertResponseWithPreviewFalseReturn(serialized_projects_full)

    def performRequests(self):
        self.response_with_preview = self.client.get(
            f'{self.target_url}?preview'
        )
        self.response_with_preview_true = self.client.get(
            f'{self.target_url}?preview=true'
        )
        self.response_with_preview_false = self.client.get(
            f'{self.target_url}?preview=false'
        )

    def assertResponsesWithPreviewReturn(self, serialized_project):
        responses = (
            self.response_with_preview, self.response_with_preview_true
        )
        assert all(
            response.data == serialized_project.data
            for response in responses
        ), 'Response data should be the same as ProjectPreviewSerializer data'

    def assertResponseWithPreviewFalseReturn(self, serialized_project):
        response_data = self.response_with_preview_false.data
        assert response_data == serialized_project.data, \
            'Response data should be the same as ProjectSerializer data'
