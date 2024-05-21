from rest_framework import serializers
from .models import Movie, Actor, Genre


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_user',)

class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ()

    def get_actors(self, obj):
        return [(actor.name, actor.db_actor_id, actor.profile_path) for actor in obj.actors.all()]

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]