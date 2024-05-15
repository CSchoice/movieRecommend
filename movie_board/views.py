from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MovieBoardArticle, MovieBoardComment
from .serializers import (
    MovieBoardArticleListSerializer,
    MovieBoardArticleSerializer, 
    MovieBoardCommentListSerializer,
    MovieBoardCommentSerializer)
from movies.models import Movie

@api_view(['GET'])
def movie_board_list(request):
    articles = MovieBoardArticle.objects.all()
    serializer = MovieBoardArticleListSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_movie_board_article(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieBoardArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def movie_board_article_detail(request, article_pk):
    article = get_object_or_404(MovieBoardArticle, pk=article_pk)
    serializer = MovieBoardArticleSerializer(article)
    return Response(serializer.data)

@api_view(['PUT'])
def edit_movie_board_article(request, article_pk):
    article = get_object_or_404(MovieBoardArticle, pk=article_pk)
    serializer = MovieBoardArticleSerializer(article, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_movie_board_article(request, article_pk):
    article = get_object_or_404(MovieBoardArticle, pk=article_pk)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_movie_board_comment(request, article_pk):
    article = get_object_or_404(MovieBoardArticle, pk=article_pk)
    serializer = MovieBoardCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_movie_board_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(MovieBoardComment, pk=comment_pk)
    serializer = MovieBoardCommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_movie_board_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(MovieBoardComment, pk=comment_pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def like_movie_board_article(request, article_pk):
    article = get_object_or_404(MovieBoardArticle, pk=article_pk)
    article.like_user.add(request.user)
    return Response(status=status.HTTP_201_CREATED)