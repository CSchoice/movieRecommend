# Generated by Django 4.2.8 on 2024-05-20 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_rename_actor_movie_actors_alter_movie_vote_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='character',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='actor',
            name='profile_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]