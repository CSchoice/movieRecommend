from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        



class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20)

    def custom_signup(self, request, user):
        nickname = self.context['request'].data.get('nickname', '')
        user.nickname = nickname
        user.save()

    def save(self, request):
        user = super().save(request)
        self.custom_signup(request, user)
        return user