from rest_framework.generics import ListAPIView

from apps.portfolio.models import Project
from apps.portfolio.serializers import ProjectSerializer


class ProjectsList(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
