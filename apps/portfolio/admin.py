from django.contrib import admin
from apps.portfolio.models import (
    Project, Technology, Screenshot
)


class ScreenshotInline(admin.StackedInline):
    model = Screenshot


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ScreenshotInline
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology)
admin.site.register(Screenshot)
