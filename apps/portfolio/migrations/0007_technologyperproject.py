# Generated by Django 3.1.5 on 2021-02-14 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_project_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnologyPerProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('how', models.TextField(max_length=4000)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.project')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.technology')),
            ],
        ),
    ]
