import re
import os

from django.test import TestCase
from django.conf import settings
from mixer.backend.django import mixer

from apps.portfolio.models import Project, Technology


class TestProjectModel(TestCase):
    def test_project_is_saved(self):
        given_project = mixer.blend(Project, name="test")
        fetched_project = Project.objects.get(name="test")
        self.assertEqual(
            given_project,
            fetched_project,
            msg='Should create a new object'
        )


class TestTechnologyModel(TestCase):
    def test_project_has_multiple_techs(self):
        five_technologies_used = mixer.cycle(5).blend(Technology)
        given_project = mixer.blend(
            Project,
            technologies=five_technologies_used
        )

        project_technologies_count = Technology.objects.filter(
            projects__pk=given_project.id
        ).count()

        self.assertEqual(
            project_technologies_count,
            5,
            msg='Project should have 5 technologies'
        )

    def tearDown(self):
        images_in_logos_directory = os.listdir(self.get_logos_directory())
        for image in images_in_logos_directory:
            self.removeImagesCreatedForTests(image)

    def get_logos_directory(self):
        return os.path.join(
            settings.MEDIA_ROOT,
            'technologies_logos'
        )

    def removeImagesCreatedForTests(self, image):
        logo_img_name_pattern = r"image(?:_\w+)?\.gif"
        if re.match(logo_img_name_pattern, image):
            os.remove(os.path.join(self.get_logos_directory(), image))
