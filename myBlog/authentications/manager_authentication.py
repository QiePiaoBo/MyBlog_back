from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from common.utils.token_util import MANAGER
from myBlog.models import Manager


class ManagerAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            token = request.query_params.get("token")

            if not str(token).startswith(MANAGER):
                print("Not manager")
                return

            user_id = cache.get(token)

            user = Manager.objects.get(user_id)

            return user, token
        except Exception as e:
            print("管理员认证失败")



