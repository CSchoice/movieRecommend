from rest_framework import serializers
from .models import MovieBoardArticle, MovieBoardComment


# class MovieBoardArticleListSerializer(serializers.ModelSerializer):
#     like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     class Meta:
#         model = MovieBoardArticle
#         # fields = ('id', 'title', 'content', 'userId')
#         fields = '__all__'

# class MovieBoardArticleSerializer(serializers.ModelSerializer):
#     like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     class Meta:
#         model = MovieBoardArticle
#         fields = '__all__'
#         read_only_fields = ('user', 'movie')

class MovieBoardCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBoardComment
        # fields = ('id', 'content', 'userId')
        fields = '__all__'
        
class MovieBoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBoardComment
        fields = '__all__'
        read_only_fields = ('user',)
