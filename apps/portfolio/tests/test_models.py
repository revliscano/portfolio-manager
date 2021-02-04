import re
import os

from django.test import TestCase
from django.conf import settings

from mixer.backend.django import mixer

from apps.portfolio.models import Project, Technology


def create_object(model, data=None):
    if data is None:
        data = {}
    return mixer.blend(model, **data)


class TestProjectModel(TestCase):
    def test_project_str_representation(self):
        project_data = {'name': 'Whatever'}
        given_project = create_object(Project, data=project_data)
        self.assertEqual(str(given_project), 'Whatever')


class TestTechnologyModel(TestCase):
    def setUp(self):
        self.tear_down_assistant = TestImagesEraser()

    def test_technology_str_representation(self):
        technology_data = {'name': 'Django'}
        given_technology = create_object(Technology, data=technology_data)
        self.assertEqual(str(given_technology), 'Django')

    def tearDown(self):
        self.tear_down_assistant.remove_logos_created_for_tests()


class TestImagesEraser:
    def remove_logos_created_for_tests(self):
        logos_directory_files = os.listdir(self.get_logos_directory())
        for image in logos_directory_files:
            self.erase(image)

    def get_logos_directory(self):
        return os.path.join(
            settings.MEDIA_ROOT,
            'technologies_logos'
        )

    def erase(self, image):
        regex_pattern_for_test_images = r"image(?:_\w+)?\.gif"
        if re.match(regex_pattern_for_test_images, image):
            os.remove(os.path.join(self.get_logos_directory(), image))
