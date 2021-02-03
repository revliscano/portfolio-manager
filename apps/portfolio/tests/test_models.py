import re
import os

from functools import partial

from django.test import TestCase
from django.conf import settings
from django.db import IntegrityError

from mixer.backend.django import mixer

from apps.portfolio.models import Project, Technology


class TestProjectModel(TestCase):
    EMPTY_LIST = []

    def test_project_is_saved(self):
        given_project = mixer.blend(Project, name="test")
        fetched_project = Project.objects.get(name="test")
        self.assertEqual(
            given_project,
            fetched_project,
            msg='Should create a new object'
        )

    def test_project_may_have_no_technologies(self):
        given_project_data = dict(
            name='some name',
            description='some description',
            year=2020
        )
        created_project = Project.objects.create(**given_project_data)

        self.assertEqual(
            list(created_project.technologies.all()),
            self.EMPTY_LIST,
            msg='Project objects should might have no technologies associated'
        )


class TestTechnologyModel(TestCase):
    FIRST_ONE = 0

    def setUp(self):
        self.tear_down_assistant = TestImagesEraser()
        self.five_different_technologies = mixer.cycle(5).blend(Technology)

    def test_project_has_multiple_techs(self):
        expected_technologies_count = 5
        given_project = mixer.blend(
            Project,
            technologies=self.five_different_technologies
        )

        project_technologies_count = Technology.objects.filter(
            projects__pk=given_project.id
        ).count()

        self.assertEqual(
            project_technologies_count,
            expected_technologies_count,
            msg='Project should have 5 technologies'
        )

    def test_project_and_tech_pair_cannot_be_repeated(self):
        given_technology = self.five_different_technologies[self.FIRST_ONE]
        given_project = mixer.blend(
            Project,
            technologies=[given_technology]
        )

        given_project.technologies.add(given_technology)

        self.assertEqual(
            list(given_project.technologies.all()),
            [given_technology]
        )

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
