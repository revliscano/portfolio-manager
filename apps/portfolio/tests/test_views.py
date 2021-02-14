from django.test import TestCase, Client
from rest_framework import status

from apps.portfolio.models import Project
from apps.portfolio.serializers import (
    ProjectSerializer,
    ProjectPreviewSerializer
)
from apps.portfolio.tests.utils import (
    create_three_objects_of,
    create_object
)


class TestOKCodeForViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_projects_url(self):
        target_url = '/api/projects/'
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_single_project_url(self):
        project = create_object(Project)
        target_url = f'/api/projects/{project.pk}/'
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

        self.assertResponsesWithPreviewReturns(serialized_projects_for_preview)
        self.assertResponseWithInvalidPreviewReturns(serialized_projects_full)

    def performRequests(self):
        self.response_with_preview = self.client.get(
            f'{self.target_url}?preview'
        )
        self.response_with_preview_true = self.client.get(
            f'{self.target_url}?preview=true'
        )
        self.response_with_preview_invalid = self.client.get(
            f'{self.target_url}?preview=invalid123'
        )

    def assertResponsesWithPreviewReturns(self, serialized_project):
        responses = (
            self.response_with_preview, self.response_with_preview_true
        )
        assert all(
            response.data == serialized_project.data
            for response in responses
        ), 'Response data should be the same as ProjectPreviewSerializer data'

    def assertResponseWithInvalidPreviewReturns(self, serialized_project):
        response_data = self.response_with_preview_invalid.data
        assert response_data == serialized_project.data, \
            'Response data should be the same as ProjectSerializer data'


def TestGetSingleProject(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = create_object(Project)

    def test_project_is_returned(self):
        expected_serializer_data = ProjectSerializer(self.project).data
        response = self.client.get(f'/api/projects/{self.project.pk}/')
        self.assertEqual(expected_serializer_data, response.data)
