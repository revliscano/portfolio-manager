from rest_framework.generics import ListAPIView

from apps.portfolio.models import Project
from apps.portfolio.serializers import (
    ProjectSerializer,
    ProjectPreviewSerializer
)


class ProjectsList(ListAPIView):
    queryset = Project.objects.all()

    @property
    def preview_mode(self):
        return (
            self.request.query_params.get('preview', 'false') in ('true', '')
        )

    def get_serializer_class(self):
        return (
            ProjectPreviewSerializer
            if self.preview_mode
            else ProjectSerializer
        )
