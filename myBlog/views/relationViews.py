from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from myBlog.authentications.user_authentication import UserAuthentication
from myBlog.models import Mark, User
from myBlog.permissions.user_permission import UserLogin
from myBlog.serializers.relationSerializer import MarkSerializer


class MarkAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    def get(self, request):
        user_id = cache.get(request.query_params.get('token'))
        user = User.objects.get(pk=user_id)
        print(user.user_name)
        marks = Mark.objects.filter(user_id=user)
        serializer = MarkSerializer(marks, many=True)
        data = {
            "msg": "OK",
            "status": 200,
            "data": serializer.data
        }

        return Response(data)

    def post(self, request):
        pass

    def delete(self,request):
        pass

