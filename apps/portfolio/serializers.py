from rest_framework import serializers

from apps.portfolio.models import Project, Technology, Screenshot


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ('id', 'project', 'image', 'is_cover', 'caption')


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    screenshots = ScreenshotSerializer(many=True)
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'year', 'technologies', 'screenshots'
        )
