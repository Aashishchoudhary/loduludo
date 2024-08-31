from rest_framework import permissions

class check_is_staff(permissions.BasePermission):
    def has_permission(self, request ,view):
      if request.user.is_staff:
         return True
