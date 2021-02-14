from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.portfolio.models import Project
from apps.portfolio.serializers import (
    ProjectSerializer,
    ProjectPreviewSerializer
)


class AllProjectsRetriever(ListAPIView):
    queryset = Project.objects.all()

    @property
    def preview_mode(self):
        return (
            self.request.query_params.get('preview') in ('true', '')
        )

    def get_serializer_class(self):
        return (
            ProjectPreviewSerializer
            if self.preview_mode
            else ProjectSerializer
        )


class SingleProjectRetriever(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
