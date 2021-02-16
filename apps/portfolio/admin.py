from django.contrib import admin
from apps.portfolio.models import (
    Project,
    Technology,
    Screenshot,
    TechnologyPerProject
)


class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 0


class TechnologyInline(admin.StackedInline):
    model = TechnologyPerProject
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        TechnologyInline,
        ScreenshotInline
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology)
admin.site.register(Screenshot)
admin.site.register(TechnologyPerProject)
