from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='technologies_logos/')

    class Meta:
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    description = models.TextField(max_length=4000)
    year = models.IntegerField()
    technologies = models.ManyToManyField(
        to=Technology,
        related_name='projects'
    )

    def __str__(self):
        return self.name


class Screenshot(models.Model):

    def generate_upload_directory(instance, filename):
        return f'screenshots/{instance.project}/{filename}'

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='screenshots'
    )
    image = models.ImageField(upload_to=generate_upload_directory)
    is_cover = models.BooleanField(default=False)
    caption = models.CharField(max_length=140)

    def __str__(self):
        return f'{self.project} screenshot'
