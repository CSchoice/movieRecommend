from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Article
        # fields = ('id', 'title', 'content', 'userId')
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('userId',)

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ('id', 'content', 'userId')
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('userId',)
