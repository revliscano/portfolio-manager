from django.test import SimpleTestCase
from django.contrib import admin as actual_admin


from apps.portfolio.models import Project, Technology, Screenshot


class MockSuperUser:
    def has_perm(self, perm):
        return True


class TestProjectAdmin(SimpleTestCase):
    def test_project_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Project))


class TestTechnologyAdmin(SimpleTestCase):
    def test_project_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Technology))


class TestScreenshotAdmin(SimpleTestCase):
    def test_project_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Screenshot))
