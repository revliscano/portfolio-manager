from django.test import SimpleTestCase
from django.contrib import admin as actual_admin
from django.forms.models import inlineformset_factory

from apps.portfolio.models import (
    Project,
    Technology,
    TechnologyPerProject,
    Screenshot
)
from apps.portfolio.admin import (
    ProjectAdmin,
    ScreenshotInline,
    TechnologyInline
)


class TestModelAdminRegistration(SimpleTestCase):
    def test_project_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Project))

    def test_technology_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Technology))

    def test_technologyperproject_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(TechnologyPerProject))

    def test_screenshot_admin_is_registered(self):
        self.assertTrue(actual_admin.site.is_registered(Screenshot))


class TestProjectAdminInlines(SimpleTestCase):

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
            parent_model=Project,
            model=Screenshot,
            fields='__all__'
        )
        project_admin_inline = self.get_project_admin_inline(ScreenshotInline)
        returned_formset = project_admin_inline.get_formset(self.request)

        self.assertEqual(type(returned_formset), type(expected_formset))

    def test_technologies_inline_is_included_in_project_admin(self):
        expected_formset = inlineformset_factory(
            parent_model=Project,
            model=TechnologyPerProject,
            fields='__all__'
        )
        project_admin_inline = self.get_project_admin_inline(TechnologyInline)
        returned_formset = project_admin_inline.get_formset(self.request)

        self.assertEqual(type(returned_formset), type(expected_formset))

    def get_project_admin_inline(self, inline):
        inline_class = next(
            inline_class
            for inline_class in ProjectAdmin.inlines
            if inline_class == inline
        )
        return inline_class(
            parent_model=Project,
            admin_site=actual_admin.site
        )
