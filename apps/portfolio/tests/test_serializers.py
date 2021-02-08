from django.test import SimpleTestCase

from apps.portfolio.models import Project
from apps.portfolio.serializers import ProjectSerializer
from apps.portfolio.tests.utils import create_object


class TestProjectSerializer(SimpleTestCase):
    def setUp(self):
        project = create_object(Project, commit=False)
        self.serializer = ProjectSerializer(project)

    def test_contains_all_fields(self):
        expected_fields = ['id', 'name', 'description', 'year', 'technologies']
        serializer_fields = self.serializer.data.keys()
        self.assertCountEqual(serializer_fields, expected_fields)
