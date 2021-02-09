from django.test import SimpleTestCase, TestCase, RequestFactory

from apps.portfolio.models import Project, Technology, Screenshot
from apps.portfolio.serializers import (
    ProjectSerializer,
    TechnologySerializer,
    ScreenshotSerializer
)
from apps.portfolio.tests.utils import (
    create_object,
    ImagesEraser,
    create_three_objects_of
)


class TestSerializersHaveDesiredFields(SimpleTestCase):
    serializers = {
        Project: ProjectSerializer,
        Technology: TechnologySerializer,
        Screenshot: ScreenshotSerializer
    }

    def test_project_serializer_contains_all_fields(self):
        expected_fields = [
            'id', 'name', 'description', 'year', 'technologies', 'screenshots'
        ]
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


class TestProjectsScreenshotSerializarion(TestCase):
    def test_multiple_screenshots_get_serialized_inside_project(self):
        self.create_project_and_screenshots()
        project_data, screenshots_data = self.get_serializers_data()
        self.assertEqual(
            project_data['screenshots'],
            screenshots_data
        )

    def create_project_and_screenshots(self):
        self.project = create_object(Project)
        self.screenshots = create_three_objects_of(
            Screenshot,
            common_data={'project': self.project}
        )

    def get_serializers_data(self):
        project_serializer = ProjectSerializer(self.project)
        screenshots_data = [
            ScreenshotSerializer(screenshot).data
            for screenshot in self.screenshots
        ]
        return project_serializer.data, screenshots_data

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name=f'screenshots/{self.project}'
        )
        tear_down_assistant.remove_whole_directory()


class TestSerializersImageFields(TestCase):
    def setUp(self):
        self.whatever_project = create_object(
            Project,
            data={'name': 'Whatever'}
        )

    def test_image_field_is_an_url(self):
        screenshot = create_object(
            Screenshot,
            data={'project': self.whatever_project}
        )
        screenshot_serializer = self.get_serializer_when_request_is_passed(
            screenshot
        )
        image_field = screenshot_serializer.data['image']

        self.assertTrue('http://testserver' in image_field)

    def get_serializer_when_request_is_passed(self, screenshot):
        request_factory = RequestFactory()
        request = request_factory.get('/')
        return ScreenshotSerializer(
            screenshot,
            context={'request': request}
        )

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='screenshots/Whatever'
        )
        tear_down_assistant.remove_whole_directory()
