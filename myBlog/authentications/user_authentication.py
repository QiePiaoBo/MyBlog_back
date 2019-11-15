from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from common.utils.token_util import USER
from myBlog.models import User


class UserAuthentication(BaseAuthentication):

    def authenticate(self, request):

        try:

            token = request.query_params.get("token")

            if not str(token).startswith(USER):

                print("Not User")

                return

            user_id = cache.get(token)

            user = User.objects.get(pk=user_id)

            return user, token

        except Exception as e:

            print("用户认证失败")

