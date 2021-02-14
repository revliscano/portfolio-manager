from django.test import TestCase, RequestFactory

from apps.portfolio.models import Project, Technology, Screenshot
from apps.portfolio.serializers import (
    ProjectSerializer,
    ProjectPreviewSerializer,
    TechnologySerializer,
    ScreenshotSerializer
)
from apps.portfolio.tests.utils import (
    create_object,
    ImagesEraser,
    create_three_objects_of
)


class TestProjectSerializerFields(TestCase):
    def setUp(self):
        project = create_object(Project)
        self.serializer = ProjectSerializer(project)

    def test_contains_all_fields(self):
        expected_fields = [
            'id', 'name', 'role', 'description', 'year',
            'technologies', 'screenshots'
        ]
        serializer_fields = self.serializer.data.keys()
        self.assertCountEqual(serializer_fields, expected_fields)


class TestProjectPreviewSerializerFields(TestCase):
    request_factory = RequestFactory()

    def setUp(self):
        request = self.request_factory.get('/')
        self.project = create_object(Project)
        self.serializer = ProjectPreviewSerializer(
            self.project,
            context={'request': request}
        )

    def test_contains_all_fields(self):
        expected_fields = ['id', 'name', 'role', 'cover_image']
        serializer_fields = self.serializer.data.keys()
        self.assertCountEqual(serializer_fields, expected_fields)

    def test_cover_image_field(self):
        screenshot = create_object(
            Screenshot,
            data={'is_cover': True, 'project': self.project}
        )
        cover_image = self.serializer.data['cover_image']
        self.assertTrue(screenshot.image.url in cover_image)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name=f'screenshots/{self.project}'
        )
        tear_down_assistant.remove_whole_directory()


class TestTechnologySerializerFields(TestCase):
    def setUp(self):
        technology = create_object(Technology)
        self.serializer = TechnologySerializer(technology)

    def test_contains_all_fields(self):
        expected_fields = ['id', 'name', 'logo']
        serializer_fields = self.serializer.data.keys()
        self.assertCountEqual(serializer_fields, expected_fields)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='technologies_logos'
        )
        tear_down_assistant.remove_images_created_for_tests()


class TestScreenshotSerializerFields(TestCase):
    def setUp(self):
        self.screenshot = create_object(Screenshot)
        self.serializer = ScreenshotSerializer(self.screenshot)

    def test_contains_all_fields(self):
        expected_fields = ['id', 'project', 'image', 'is_cover', 'caption']
        serializer_fields = self.serializer.data.keys()
        self.assertCountEqual(serializer_fields, expected_fields)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name=f'screenshots/{self.screenshot.project}'
        )
        tear_down_assistant.remove_whole_directory()


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


class TestProjectsTechnologiesSerializarion(TestCase):
    def test_multiple_technologies_get_serialized_inside_project(self):
        self.create_project_and_technologies()
        project_data, technologies_data = self.get_serializers_data()
        self.assertEqual(
            project_data['technologies'],
            technologies_data
        )

    def create_project_and_technologies(self):
        self.technologies = create_three_objects_of(Technology)
        self.project = create_object(
            Project,
            data={'technologies': self.technologies}
        )

    def get_serializers_data(self):
        project_serializer = ProjectSerializer(self.project)
        technologies_data = [
            TechnologySerializer(technology).data
            for technology in self.technologies
        ]
        return project_serializer.data, technologies_data

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='technologies_logos'
        )
        tear_down_assistant.remove_images_created_for_tests()
