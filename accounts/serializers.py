from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate

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


class CustomLoginSerializer(LoginSerializer):

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # username이 있는지 확인
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                'message': '존재하지 않는 사용자 이름입니다.'
            })

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({
                'message': '비밀번호가 틀렸습니다.'
            })

        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')

        data['user'] = user
        return data