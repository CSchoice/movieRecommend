from rest_framework import serializers
from .models import FreeBoardArticle, FreeBoardComment

class FreeBoardArticleListSerializer(serializers.ModelSerializer):
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments_cnt = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()   

    class Meta:
        model = FreeBoardArticle
        fields = '__all__'

    def get_comments_cnt(self, obj):
        return FreeBoardComment.objects.filter(article=obj).count()

    def get_user_nickname(self, obj):
        return obj.user.nickname if obj.user else None

    def get_username(self, obj):
        return obj.user.username if obj.user else None

class FreeBoardArticleSerializer(serializers.ModelSerializer):
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user_nickname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()   

    class Meta:
        model = FreeBoardArticle
        fields = '__all__'
        read_only_fields = ('user',)
        
    def get_user_nickname(self, obj):
        return obj.user.nickname if obj.user else None
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None


class FreeBoardCommentListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()   
    
    class Meta:
        model = FreeBoardComment
        fields = '__all__'
    
    def get_user_nickname(self, obj):
        return obj.user.nickname if obj.user else None

    def get_username(self, obj):
        return obj.user.username if obj.user else None

class FreeBoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeBoardComment
        fields = '__all__'
        read_only_fields = ('user', 'article')