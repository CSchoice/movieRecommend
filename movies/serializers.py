from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_user',)