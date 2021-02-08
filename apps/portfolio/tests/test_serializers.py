from django.test import SimpleTestCase, TestCase, RequestFactory

from apps.portfolio.models import Project, Technology, Screenshot
from apps.portfolio.serializers import (
    ProjectSerializer,
    TechnologySerializer,
    ScreenshotSerializer
)
from apps.portfolio.tests.utils import create_object, ImagesEraser


class TestSerializers(SimpleTestCase):
    serializers = {
        Project: ProjectSerializer,
        Technology: TechnologySerializer,
        Screenshot: ScreenshotSerializer
    }

    def test_project_serializer_contains_all_fields(self):
        expected_fields = ['id', 'name', 'description', 'year', 'technologies']
        serializer_fields = self.get_serializer_fields_for(Project)
        self.assertCountEqual(serializer_fields, expected_fields)

    def test_technology_serializer_contains_all_fields(self):
        expected_fields = ['id', 'name', 'logo']
        serializer_fields = self.get_serializer_fields_for(Technology)
        self.assertCountEqual(serializer_fields, expected_fields)

    def test_screenshot_serializer_contains_all_fields(self):
        expected_fields = ['id', 'project', 'image', 'is_cover', 'caption']
        serializer_fields = self.get_serializer_fields_for(Screenshot)
        self.assertCountEqual(serializer_fields, expected_fields)

    def get_serializer(self, model):
        object_ = create_object(model, commit=False)
        return self.serializers[model](object_)

    def get_serializer_fields_for(self, model):
        serializer = self.get_serializer(model)
        return serializer.data.keys()


class TestScreenshotSerializerImages(TestCase):
    request_factory = RequestFactory()

    def setUp(self):
        self.request = self.request_factory.get('/')
        self.whatever_project = create_object(
            Project,
            data={'name': 'Whatever'}
        )

    def test_image_field_is_an_url(self):
        screenshot = create_object(
            Screenshot,
            data={'project': self.whatever_project}
        )
        screenshot_serializer = ScreenshotSerializer(
            screenshot,
            context={'request': self.request}
        )
        image_field = screenshot_serializer.data['image']

        self.assertTrue('http://testserver' in image_field)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='screenshots/Whatever'
        )
        tear_down_assistant.remove_whole_directory()
