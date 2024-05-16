from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MovieBoardComment
from .serializers import (
    MovieBoardCommentListSerializer,
    MovieBoardCommentSerializer)
from movies.models import Movie

@api_view(['GET'])
def movie_board_comment_list(request, movie_pk):
    comments = MovieBoardComment.objects.filter(movie_id=movie_pk)
    serializer = MovieBoardCommentListSerializer(comments, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def movie_board_list(request):
#     articles = MovieBoardArticle.objects.all()
#     serializer = MovieBoardArticleListSerializer(articles, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_movie_board_article(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     serializer = MovieBoardArticleSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=request.user, movie=movie)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def movie_board_article_detail(request, article_pk):
#     article = get_object_or_404(MovieBoardArticle, pk=article_pk)
#     serializer = MovieBoardArticleSerializer(article)
#     return Response(serializer.data)

# @api_view(['PUT', 'DELETE'])
# def edit_movie_board_article(request, article_pk):
#     if request.method == 'PUT':
#         article = get_object_or_404(MovieBoardArticle, pk=article_pk)
#         serializer = MovieBoardArticleSerializer(article, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         article.delete()
#         return Response({"message": "게시글 삭제 성공"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_movie_board_comment(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    serializer = MovieBoardCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
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

# @api_view(['POST'])
# def like_movie_board_article(request, article_pk):
#     article = get_object_or_404(MovieBoardArticle, pk=article_pk)
#     if article.like_user.filter(pk=request.user.pk).exists():
#         # 이미 좋아요를 한 경우, 좋아요 취소
#         article.like_user.remove(request.user)
#         return Response({"message": "게시글 좋아요 취소"}, status=status.HTTP_200_OK)
#     else:
#         # 좋아요 추가
#         article.like_user.add(request.user)
#         return Response({"message": "게시글 좋아요 성공"}, status=status.HTTP_200_OK)
    