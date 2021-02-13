from django.urls import path
from apps.portfolio.views import ProjectsList


urlpatterns = [
    path('projects/', ProjectsList.as_view(), name='get_all_projects')
]
