from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.portfolio.models import (
    Project,
    Technology,
    TechnologyPerProject,
    Screenshot
)


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = '__all__'


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


class TechnologyPerProjectSerializer(serializers.ModelSerializer):
    technology_name = serializers.ReadOnlyField(source='technology.name')
    technology_logo = serializers.SerializerMethodField()

    class Meta:
        model = TechnologyPerProject
        fields = ('id', 'how', 'technology_name', 'technology_logo')

    def get_technology_logo(self, technology_being_serialized):
        relative_uri = technology_being_serialized.technology.logo.url
        try:
            absolute_uri = self.context['request'].build_absolute_uri(
                relative_uri
            )
            return absolute_uri
        except KeyError:
            return relative_uri


class ProjectSerializer(serializers.ModelSerializer):
    screenshots = ScreenshotSerializer(many=True)
    technologies = TechnologyPerProjectSerializer(
        many=True,
        source='technologies_per_project'
    )

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'role', 'description', 'year',
            'technologies', 'screenshots'
        )


class ProjectPreviewSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'role', 'cover_image')

    def get_cover_image(self, project_being_serialized):
        try:
            screenshot = Screenshot.objects.get(
                project=project_being_serialized,
                is_cover=True
            )
            return self.context['request'].build_absolute_uri(
                screenshot.image.url
            )
        except ObjectDoesNotExist:
            return ''
