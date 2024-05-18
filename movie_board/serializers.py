from rest_framework import serializers
from .models import MovieBoardComment


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
    comments_cnt = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    class Meta:
        model = MovieBoardComment
        # fields = ('id', 'content', 'userId')
        fields = '__all__'

    def get_comments_cnt(self, obj):
        return MovieBoardComment.objects.filter(movie=obj.movie).count()

    def get_user_nickname(self, obj):
        return obj.user.nickname if obj.user else None
        
class MovieBoardCommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()
    class Meta:
        model = MovieBoardComment
        fields = '__all__'
        read_only_fields = ('user', 'movie')
        
    def get_user_nickname(self, obj):
        return obj.user.nickname if obj.user else None

