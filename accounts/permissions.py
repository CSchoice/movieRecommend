from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsEditorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'editor']

class IsViewerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'editor', 'viewer']
    
    
# view에서 사용법 예시
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .permissions import IsAdminUser, IsEditorUser, IsViewerUser

# class AdminOnlyView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         return Response({"message": "Hello, Admin!"})

# class EditorOnlyView(APIView):
#     permission_classes = [IsEditorUser]

#     def get(self, request):
#         return Response({"message": "Hello, Editor!"})

# class ViewerOnlyView(APIView):
#     permission_classes = [IsViewerUser]

#     def get(self, request):
#         return Response({"message": "Hello, Viewer!"})