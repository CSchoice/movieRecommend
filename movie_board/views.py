from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import MovieBoardComment
from .serializers import (
    MovieBoardCommentListSerializer,
    MovieBoardCommentSerializer)
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def movie_board_comment_list(request, movie_pk):
    comments = MovieBoardComment.objects.filter(movie_id=movie_pk).order_by('-created_at')
    serializer = MovieBoardCommentListSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_movie_board_comment(request, movie_id):
    movie = get_object_or_404(Movie, db_movie_id=movie_id)
    serializer = MovieBoardCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def edit_movie_board_comment(request, movie_id, comment_pk):
    comment = get_object_or_404(MovieBoardComment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = MovieBoardCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        comment.delete()
        return Response({"message": "댓글 삭제 성공"}, status=status.HTTP_200_OK)
    