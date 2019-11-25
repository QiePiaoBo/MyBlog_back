from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response

from common.utils.token_util import MANAGER
from myBlog.models import Manager


class ManagerAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            token = request.query_params.get("token")

            if not str(token).startswith(MANAGER):
                print("Not manager")
                return Response("Not manager")

            manager_id = int(cache.get(token))

            manager = Manager.objects.get(pk=manager_id)

            return manager, token
        except Exception as e:
            print(e)
            print("------管理员认证失败")
