from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FreeBoardArticle, FreeBoardComment
from .serializers import (
    FreeBoardArticleListSerializer,
    FreeBoardArticleSerializer,
    FreeBoardCommentSerializer,
    FreeBoardCommentListSerializer,
)

# 전체 게시물 조회
@api_view(['GET'])
def list_articles(request):
    articles = FreeBoardArticle.objects.all()
    serializer = FreeBoardArticleListSerializer(articles, many=True)
    return Response(serializer.data)

# 게시글 작성
@api_view(['POST'])
def create_article(request):
    serializer = FreeBoardArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(userId=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 정보 조회
@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    serializer = FreeBoardArticleSerializer(article)
    return Response(serializer.data)

# 게시글 수정
@api_view(['PUT'])
def update_article(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    serializer = FreeBoardArticleSerializer(article, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 삭제
@api_view(['DELETE'])
def delete_article(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 작성
@api_view(['POST'])
def create_comment(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    serializer = FreeBoardCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(article=article, userId=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 수정
@api_view(['PUT'])
def update_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(FreeBoardComment, pk=comment_pk, article_id=article_pk)
    serializer = FreeBoardCommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 삭제
@api_view(['DELETE'])
def delete_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(FreeBoardComment, pk=comment_pk, article_id=article_pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)