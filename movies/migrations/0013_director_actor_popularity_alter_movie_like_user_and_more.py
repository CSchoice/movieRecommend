# Generated by Django 4.2.8 on 2024-05-21 04:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0012_remove_movie_like_user_movie_like_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('db_director_id', models.IntegerField(unique=True)),
                ('profile_path', models.CharField(blank=True, max_length=200, null=True)),
                ('job', models.CharField(blank=True, max_length=40, null=True)),
                ('popularity', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='actor',
            name='popularity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='like_user',
            field=models.ManyToManyField(related_name='liked_movies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(blank=True, to='movies.director'),
        ),
    ]
