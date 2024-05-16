from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_control(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, tar_user_pk):
    follower = request.user
    following = get_object_or_404(User, pk=tar_user_pk)
    
    if following in follower.followings.all():
        follower.followings.remove(following)
        message = "팔로우 취소"
    else:
        follower.followings.add(following)
        message = "팔로우 성공"
    
    follower.save()
    return Response({"message": message}, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_login(request):
    if request.user.is_authenticated:
        return Response({"message": "로그인 됨."}, status=status.HTTP_200_OK)
    return Response({"message": "로그인 되지 않음"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request, tar_username):
    user = get_object_or_404(User, username=tar_username)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_followings(request, tar_username):
    user = get_object_or_404(User, username=tar_username)
    followings = user.followings.all()
    serializer = UserSerializer(followings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_followers(request, tar_username):
    user = get_object_or_404(User, username=tar_username)
    followers = user.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)