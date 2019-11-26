from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myBlog.authentications.user_authentication import UserAuthentication
from myBlog.models import Mark, User
from myBlog.permissions.user_permission import UserLogin
from myBlog.serializers.relationSerializer import MarkSerializer


# 收藏增删改查
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
        user_id = cache.get(request.query_params.get('token'))
        fav_blog = request.data.get("fav_blog")
        req_data = {
            "user_id": user_id,
            "fav_blog": fav_blog
        }
        Marks = Mark.objects.filter(user_id=user_id).filter(fav_blog=fav_blog)
        if len(Marks) > 0:
            return Response("数据重复")
        serializer = MarkSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            resp_data = {
                "status": 200,
                "msg": "Added",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            resp_data = {
                "status": 403,
                "msg": "Failed"
            }
            return Response(resp_data)

    def delete(self, request):
        user_token = request.query_params.get("token")
        user_id = cache.get(user_token)
        fav_blog = request.data.get("fav_blog")
        mark = Mark.objects.filter(user_id=user_id).filter(fav_blog=fav_blog).first()
        print(mark)
        if mark:
            mark.delete()
            resp_data = {
                "status": status.HTTP_200_OK,
                "msg": "Deleted",
                "data": MarkSerializer(mark).data
            }
            return Response(resp_data)
        else:
            resp_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": "Not Deleted",
                "data": request.data
            }
            return Response(resp_data)
