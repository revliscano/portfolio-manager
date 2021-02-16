from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='technologies_logos/')

    class Meta:
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.delete_actual_logo_file()
        super().delete(*args, **kwargs)

    def delete_actual_logo_file(self):
        self.logo.delete(save=True)


class Project(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    description = models.TextField(max_length=4000)
    year = models.IntegerField()
    technologies = models.ManyToManyField(
        to=Technology,
        through='TechnologyPerProject',
        related_name='projects'
    )

    def __str__(self):
        return self.name


class TechnologyPerProject(models.Model):
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='technologies_per_project'
    )
    technology = models.ForeignKey(
        to=Technology,
        on_delete=models.CASCADE
    )
    how = models.TextField(max_length=4000)

    class Meta:
        verbose_name_plural = 'Technologies Per Project'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'technology'],
                name='unique_project_and_technology_pair'
            )
        ]

    def __str__(self):
        return f'{self.technology} on {self.project}'


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

    def delete(self, *args, **kwargs):
        self.delete_actual_image_file()
        super().delete(*args, **kwargs)

    def delete_actual_image_file(self):
        self.image.delete(save=True)
