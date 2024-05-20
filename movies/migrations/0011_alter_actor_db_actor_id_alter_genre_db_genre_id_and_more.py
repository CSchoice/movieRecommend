# Generated by Django 4.2.8 on 2024-05-20 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_rename_actor_id_actor_db_actor_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='db_actor_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='db_genre_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='db_movie_id',
            field=models.IntegerField(unique=True),
        ),
    ]
