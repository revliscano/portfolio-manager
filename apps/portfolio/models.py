from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='technologies_logos/')


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=4000)
    year = models.IntegerField()
    technologies = models.ManyToManyField(
        to=Technology,
        related_name='projects'
    )
