from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # 사용자가 인증되었는지와 역할이 'admin'인지 확인합니다.
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsEditorUser(BasePermission):
    def has_permission(self, request, view):
        # 사용자가 인증되었는지와 역할이 'editor' 또는 'admin'인지 확인합니다.
        return request.user and request.user.is_authenticated and (request.user.role == 'editor' or request.user.role == 'admin')

class IsViewerUser(BasePermission):
    def has_permission(self, request, view):
        # 사용자가 인증되었는지와 역할이 'viewer' 또는 'editor' 또는 'admin'인지 확인합니다.
        return request.user and request.user.is_authenticated and (request.user.role == 'viewer' or request.user.role in ['editor', 'admin'])
    
    
# view에서 사용법 예시
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response

# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def admin_only_view(request):
#     return Response({"message": "Hello, Admin!"})

# @api_view(['GET'])
# @permission_classes([IsEditorUser])
# def editor_only_view(request):
#     return Response({"message": "Hello, Editor!"})

# @api_view(['GET'])
# @permission_classes([IsViewerUser])
# def viewer_only_view(request):
#     return Response({"message": "Hello, Viewer!"})