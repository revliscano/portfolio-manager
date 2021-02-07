from django.contrib import admin
from apps.portfolio.models import (
    Project, Technology, Screenshot
)


admin.site.register(Project)
admin.site.register(Technology)
admin.site.register(Screenshot)
