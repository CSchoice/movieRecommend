# Generated by Django 4.2.8 on 2024-05-20 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_movie_actor_alter_movie_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(null=True),
        ),
    ]
