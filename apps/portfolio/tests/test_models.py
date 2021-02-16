from os.path import dirname, exists
from unittest import skip as skip_test

from django.test import TestCase
from django.db.utils import IntegrityError

from apps.portfolio.models import (
    Project,
    Technology,
    Screenshot,
    TechnologyPerProject
)
from apps.portfolio.tests.utils import (
    create_object,
    create_three_objects_of,
    ImagesEraser,
    ImagePath
)


class TestProjectModel(TestCase):
    def test_object_str_representation(self):
        given_project = create_object(
            Project,
            data={'name': 'Whatever'}
        )
        self.assertEqual(str(given_project), 'Whatever')


class TestTechnologyModel(TestCase):
    def test_object_str_representation(self):
        given_technology = create_object(
            Technology,
            data={'name': 'Django'}
        )
        self.assertEqual(str(given_technology), 'Django')

    def test_plural_str_representation(self):
        expected_plural_name = 'Technologies'
        model_plural_name = Technology._meta.verbose_name_plural
        self.assertEqual(model_plural_name, expected_plural_name)

    def tearDown(self):
        tear_down_assistant = ImagesEraser(
            directory_name='technologies_logos'
        )
        tear_down_assistant.remove_images_created_for_tests()


class TestTechnologyPerProject(TestCase):
    def setUp(self):
        self.project = create_object(
            Project,
            data={'name': 'My Project'}
        )
        self.technology = create_object(
            Technology,
            data={'name': 'JS'}
        )
        self.project_technology = create_object(
            TechnologyPerProject,
            data={
                'project': self.project,
                'technology': self.technology
            }
        )

    def test_object_str_representation(self):
        expected_str = f'{self.technology} on {self.project}'
        self.assertEqual(str(self.project_technology), expected_str)

    def test_plural_str_representation(self):
        expected_plural_name = 'Technologies Per Project'
        model_plural_name = TechnologyPerProject._meta.verbose_name_plural
        self.assertEqual(model_plural_name, expected_plural_name)

    def test_unique_project_technology_pair_constraint(self):
        self.assertRaises(
            IntegrityError,
            self.try_to_create_a_repeated_project_technology_pair
        )

    def try_to_create_a_repeated_project_technology_pair(self):
        TechnologyPerProject.objects.create(
            project=self.project,
            technology=self.technology
        )

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

    def test_object_str_representation(self):
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


class TestTechnologyLogoFileDeletion(TestCase):
    def test_logo_gets_deleted_on_technology_deletion(self):
        technology = create_object(Technology)
        image_path = ImagePath(technology.logo.url)

        technology.delete()

        self.assertFalse(exists(image_path.absolute_path))


class TestScreenshotsImagesFileDeletion(TestCase):
    def test_image_gets_deleted_on_screenshot_deletion(self):
        screenshot = create_object(Screenshot)
        image_path = ImagePath(screenshot.image.url)

        screenshot.delete()

        self.assertFalse(exists(image_path.absolute_path))

    def test_all_images_get_deleted_on_project_deletion(self):
        project = create_object(Project)
        screenshots = create_three_objects_of(
            Screenshot,
            common_data={'project': project}
        )

        project.delete()

        self.assertTrue(self.all_images_were_deleted(screenshots))

    def all_images_were_deleted(self, screenshots):
        images_paths = self.get_images_paths(screenshots)
        return all(
            exists(image_path.absolute_path) is False
            for image_path in images_paths
        )

    def get_images_paths(self, screenshots):
        return [
            ImagePath(screenshot.image.url)
            for screenshot in screenshots
        ]
