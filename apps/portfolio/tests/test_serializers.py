from django.test import SimpleTestCase

from apps.portfolio.models import Project, Technology
from apps.portfolio.serializers import (
    ProjectSerializer,
    TechnologySerializer
)
from apps.portfolio.tests.utils import create_object


class TestSerializers(SimpleTestCase):
    def setUp(self):
        self.serializers = {
            Project: ProjectSerializer,
            Technology: TechnologySerializer
        }

    def test_project_serializer_contains_all_fields(self):
        expected_fields = ['id', 'name', 'description', 'year', 'technologies']
        serializer_fields = self.get_serializer_fields_for(Project)
        self.assertCountEqual(serializer_fields, expected_fields)

    def test_technology_serializer_contains_all_fields(self):
        expected_fields = ['id', 'name', 'logo']
        serializer_fields = self.get_serializer_fields_for(Technology)
        self.assertCountEqual(serializer_fields, expected_fields)

    def get_serializer_fields_for(self, model):
        object_ = create_object(model, commit=False)
        serializer = self.serializers[model](object_)
        return serializer.data.keys()
