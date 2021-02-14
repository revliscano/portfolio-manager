from django.urls import path
from apps.portfolio.views import (
    AllProjectsRetriever,
    SingleProjectRetriever
)


urlpatterns = [
    path(
        'projects/',
        AllProjectsRetriever.as_view(),
        name='get_all_projects'
    ),
    path(
        'projects/<int:pk>/',
        SingleProjectRetriever.as_view(),
        name='get_single_project'
    )
]
