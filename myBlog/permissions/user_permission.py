from django.core.cache import cache
from rest_framework.permissions import BasePermission

from myBlog.models import User


class UserLogin(BasePermission):

    def has_permission(self, request, view):
        return isinstance(request.user, User)


