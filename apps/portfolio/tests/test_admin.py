from django.test import SimpleTestCase
from django.contrib import admin as actual_admin
from django.forms.models import inlineformset_factory

from apps.portfolio.models import Project, Technology, Screenshot
from apps.portfolio.admin import ProjectAdmin


class TestModelAdminRegistration(SimpleTestCase):
    def test_project_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Project))

    def test_technology_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Technology))

    def test_screenshot_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Screenshot))


class TestScreenshotsInline(SimpleTestCase):
    FIRST_INLINE = 0

    class MockRequest:
        pass

    class MockSuperUser:
        def has_perm(self, perm, obj=None):
            return True

    def setUp(self):
        self.request = self.MockRequest()
        self.request.user = self.MockSuperUser()

    def test_screenshots_inline_is_included_in_project_admin(self):
        expected_formset = inlineformset_factory(
            Project,
            Screenshot,
            fields='__all__'
        )

        inline = self.get_project_admin_inline()
        formset = inline.get_formset(self.request)

        self.assertEqual(type(formset), type(expected_formset))

    def get_project_admin_inline(self):
        inline_class = ProjectAdmin.inlines[self.FIRST_INLINE]
        return inline_class(Project, actual_admin.site)
