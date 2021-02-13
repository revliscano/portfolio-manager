from rest_framework import serializers

from apps.portfolio.models import Project, Technology, Screenshot


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        # colocar '__all__ en vez de hardcodear los fields'
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
            'id', 'name', 'role', 'description', 'year',
            'technologies', 'screenshots'
        )


class ProjectPreviewSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'role', 'cover_image')

    def get_cover_image(self, project_being_serialized):
        screenshot = Screenshot.objects.filter(
            project=project_being_serialized,
            is_cover=True
        ).first()
        if screenshot is None:
            return None
        return screenshot.image.url
