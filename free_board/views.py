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
def free_board_list(request):
    articles = FreeBoardArticle.objects.all()
    serializer = FreeBoardArticleListSerializer(articles, many=True)
    return Response(serializer.data)

# 게시글 작성
@api_view(['POST'])
def create_free_board_article(request):
    serializer = FreeBoardArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(userId=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 정보 조회
@api_view(['GET'])
def free_board_article_detail(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    serializer = FreeBoardArticleSerializer(article)
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def edit_free_board_article(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    # 게시글 수정
    if request.method == 'PUT':
        serializer = FreeBoardArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 게시글 삭제
    else:
        article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 작성
@api_view(['POST'])
def create_free_board_comment(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    serializer = FreeBoardCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(article=article, userId=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def edit_free_board_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(FreeBoardComment, pk=comment_pk, article_id=article_pk)
    # 댓글 수정
    if request.method == 'PUT':   
        serializer = FreeBoardCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 댓글 삭제
    else:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def like_free_board_article(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    if article.like_user.filter(pk=request.user.pk).exists():
        # 이미 좋아요를 한 경우, 좋아요 취소
        article.like_user.remove(request.user)
        return Response({"message": "게시글 좋아요 취소"}, status=status.HTTP_200_OK)
    else:
        # 좋아요 추가
        article.like_user.add(request.user)
        return Response({"message": "게시글 좋아요 성공"}, status=status.HTTP_200_OK)