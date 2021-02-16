from importlib import import_module

from django.apps import AppConfig
from django.db.models.signals import pre_delete


class PortfolioConfig(AppConfig):
    name = 'apps.portfolio'

    def ready(self):
        Project = self.get_model('Project')
        portfolio_signals = import_module('apps.portfolio.signals')

        pre_delete.connect(
            portfolio_signals.delete_screenshot_image_on_project_deletion,
            sender=Project
        )
