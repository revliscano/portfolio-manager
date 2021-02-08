from os.path import dirname

from django.test import TestCase

from apps.portfolio.models import Project, Technology, Screenshot
from apps.portfolio.tests.utils import create_object, ImagesEraser


class TestProjectModel(TestCase):
    def test_project_str_representation(self):
        given_project = create_object(
            Project,
            data={'name': 'Whatever'}
        )
        self.assertEqual(str(given_project), 'Whatever')


class TestTechnologyModel(TestCase):
    def test_technology_str_representation(self):
        given_technology = create_object(
            Technology,
            data={'name': 'Django'}
        )
        self.assertEqual(str(given_technology), 'Django')

    def test_technology_plural_str_representation(self):
        expected_plural_name = 'Technologies'
        model_plural_name = Technology._meta.verbose_name_plural
        self.assertEqual(model_plural_name, expected_plural_name)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='technologies_logos'
        )
        tear_down_assistant.remove_images_created_for_tests()


class TestScreenshotModel(TestCase):
    def setUp(self):
        self.whatever_project = create_object(
            Project,
            data={'name': 'Whatever'}
        )

    def test_screenshot_str_representation(self):
        screenshot = create_object(
            Screenshot,
            data={'project': self.whatever_project}
        )
        self.assertEqual(str(screenshot), 'Whatever screenshot')

    def test_screenshots_are_saved_in_project_subdirectory(self):
        screenshot = create_object(
            Screenshot,
            data={'project': self.whatever_project}
        )
        uploaded_image_directory_path = dirname(screenshot.image.url)
        self.assertEqual(
            self.get_last_two_components_of(uploaded_image_directory_path),
            'screenshots/Whatever'
        )

    def get_last_two_components_of(self, uploaded_image_directory_path):
        components = uploaded_image_directory_path.split('/')[-2:]
        return '/'.join(components)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='screenshots/Whatever'
        )
        tear_down_assistant.remove_whole_directory()
