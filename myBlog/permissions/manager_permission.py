from django.core.cache import cache
from rest_framework.permissions import BasePermission

from myBlog.models import Manager


class ManagerLogin(BasePermission):

    def has_permission(self, request, view):
        return isinstance(request.user, Manager)


