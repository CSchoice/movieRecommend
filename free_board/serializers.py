from rest_framework import serializers
from .models import FreeBoardArticle, FreeBoardComment

class FreeBoardArticleListSerializer(serializers.ModelSerializer):
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = FreeBoardArticle
        fields = '__all__'

class FreeBoardArticleSerializer(serializers.ModelSerializer):
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = FreeBoardArticle
        fields = '__all__'
        read_only_fields = ('userId',)

class FreeBoardCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeBoardComment
        fields = '__all__'
        
class FreeBoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeBoardComment
        fields = '__all__'
        read_only_fields = ('userId',)