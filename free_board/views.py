from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import FreeBoardArticle, FreeBoardComment
from .serializers import (
    FreeBoardArticleListSerializer,
    FreeBoardArticleSerializer,
    FreeBoardCommentSerializer,
    FreeBoardCommentListSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

# 전체 게시물 조회
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def free_board_list(request):
    articles = FreeBoardArticle.objects.all().order_by('-created_at')
    serializer = FreeBoardArticleListSerializer(articles, many=True)
    return Response(serializer.data)

# 게시글 작성
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_free_board_article(request):
    serializer = FreeBoardArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 정보 조회
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def free_board_article_detail(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    comments = FreeBoardComment.objects.filter(article=article).order_by('-created_at')
    article_serializer = FreeBoardArticleSerializer(article)
    comment_serializer = FreeBoardCommentListSerializer(comments, many=True)
    return Response({'article': article_serializer.data, 'comments': comment_serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
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
        return Response({"message": "게시글 삭제 성공"}, status=status.HTTP_200_OK)

# 댓글 작성
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_free_board_comment(request, article_pk):
    article = get_object_or_404(FreeBoardArticle, pk=article_pk)
    serializer = FreeBoardCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
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
        return Response({"message": "댓글 삭제 성공"}, status=status.HTTP_200_OK)

    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
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