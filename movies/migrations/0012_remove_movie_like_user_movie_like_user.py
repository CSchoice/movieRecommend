# Generated by Django 4.2.8 on 2024-05-20 07:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0011_alter_actor_db_actor_id_alter_genre_db_genre_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='like_user',
        ),
        migrations.AddField(
            model_name='movie',
            name='like_user',
            field=models.ManyToManyField(null=True, related_name='liked_movies', to=settings.AUTH_USER_MODEL),
        ),
    ]