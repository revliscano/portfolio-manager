from django.test import TestCase
from mixer.backend.django import mixer

from apps.portfolio.models import Project, Technology


class TestProjectModel(TestCase):
    def test_project_is_saved(self):
        given_project = mixer.blend(Project, name="test")
        fetched_project = Project.objects.get(name="test")
        self.assertEqual(given_project, fetched_project)

    def test_project_has_multiple_techs(self):
        five_technologies_used = mixer.cycle(5).blend(Technology)
        given_project = mixer.blend(
            Project,
            technologies=five_technologies_used
        )

        project_technologies_count = Technology.objects.filter(
            projects__pk=given_project.id
        ).count()

        self.assertEqual(project_technologies_count, 5)
