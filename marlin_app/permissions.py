from rest_framework import permissions

class IsAuthenticatedOrOwner(permissions.BasePermission):

    def has_permission (self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        if request.user and request.user.is_authenticated:
            return request.user.userprofile.usertype == 1