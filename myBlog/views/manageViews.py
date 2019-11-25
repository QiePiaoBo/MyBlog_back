from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myBlog.authentications.manager_authentication import ManagerAuthentication
from myBlog.models import BlogType, Blog, User, SystemNotice, Manager
from myBlog.permissions.manager_permission import ManagerLogin
from myBlog.serializers.blogSerializer import BlogTypeSerializer, BlogSerializer

# blog_type
from myBlog.serializers.relationSerializer import SystemNoticeSerializer
from myBlog.serializers.userSerializer import UserSerializer


class ManageBlogTypeAPIView(APIView):
    authentication_classes = [ManagerAuthentication, ]
    permission_classes = [ManagerLogin, ]

    def get(self, request):
        blog_types = BlogType.objects.all()
        blog_type_serializers = BlogTypeSerializer(blog_types, many=True)

        return Response(blog_type_serializers.data)

    def post(self, request):
        req_data = request.data
        serializer = BlogTypeSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            resp_data = {
                "status": status.HTTP_201_CREATED,
                "msg": "添加类型成功",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            return Response(req_data)

    def put(self, request):
        req_data = request.data
        blog_type_id = req_data.get('id')
        type = BlogType.objects.get(pk=blog_type_id)
        serializer = BlogTypeSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        if serializer.update(type, serializer.validated_data):
            resp_data = {
                "status": status.HTTP_205_RESET_CONTENT,
                "msg": "Updated Ok",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            resp_data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "Failed",
                "data": req_data
            }
            return Response(resp_data)

    def delete(self, request):
        type_id = request.data.get("id")
        blog_type = BlogType.objects.get(pk=type_id)
        serializer = BlogTypeSerializer(blog_type)
        if blog_type.delete():
            resp_data = {
                "status": status.HTTP_200_OK,
                "msg": "Deleted",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            return Response("Failed")


# blog
class ManageBlogAPIView(APIView):
    authentication_classes = [ManagerAuthentication, ]
    permission_classes = [ManagerLogin, ]

    def get(self, request):
        page_number = request.query_params.get("page_number")
        page_size = request.query_params.get("page_size")
        blogs = Blog.objects.all()
        blog_list = Paginator(blogs, per_page=page_size)
        page_blogs = blog_list.page(page_number)

        result = []
        for p in page_blogs:
            serizlizer = BlogSerializer(p)
            result.append(serizlizer.data)
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Query Ok",
            "data": result,
            "total_number": blog_list.count,
            "total_page": blog_list.num_pages
        }

        return Response(resp_data)

    def put(self, request):
        action = request.query_params.get("action")

        if action == "top":
            return self.make_top(request)
        elif action == "not_top":
            return self.make_not_top(request)
        else:
            return Response("请求类型错误,仅置顶和非置顶可选")

    def make_top(self, request):
        req_data = request.data
        blog_id = req_data.get('id')
        blog = Blog.objects.get(pk=blog_id)

        blog.blog_top = True
        blog.save()
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Saved",
            "data": req_data
        }
        return Response(resp_data)

    def make_not_top(self, request):
        req_data = request.data
        blog_id = req_data.get('id')
        blog = Blog.objects.get(pk=blog_id)

        blog.blog_top = False
        blog.save()
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Changed",
            "data": req_data
        }
        return Response(resp_data)

    def delete(self, request):
        blog_id = request.data.get("id")
        blog = Blog.objects.get(pk=blog_id)
        serializer = BlogSerializer(blog)
        if blog.delete():
            resp_data = {
                "status": status.HTTP_200_OK,
                "msg": "Deleted",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            return Response("Failed")


# user
class ManageUserAPIView(APIView):
    authentication_classes = [ManagerAuthentication, ]
    permission_classes = [ManagerLogin, ]

    def get(self, request):
        page_number = request.query_params.get("page_number")
        page_size = request.query_params.get("page_size")
        users = User.objects.all()
        user_list = Paginator(users, per_page=page_size)
        page_users = user_list.page(page_number)

        result = []
        for u in page_users:
            serizlizer = UserSerializer(u)
            result.append(serizlizer.data)
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Query Ok",
            "data": result,
            "total_number": user_list.count,
            "total_page": user_list.num_pages
        }

        return Response(resp_data)

    def put(self, request):
        action = request.query_params.get("action")
        if action == "lock":
            return self.lock(request)
        elif action == "unlock":
            return self.unlock(request)
        elif action == "freeze":
            return self.disable(request)
        elif action == "unfreeze":
            return self.enable(request)
        else:
            return Response("参数错误")

    def lock(self, request):
        req_data = request.data
        user_id = req_data.get('id')
        user = User.objects.get(pk=user_id)
        user.user_lock = True
        user.save()
        resp_data = {
            "status": status.HTTP_205_RESET_CONTENT,
            "msg": "Updated Ok",
            "data": UserSerializer(user).data
        }
        return Response(resp_data)

    def unlock(self, request):
        req_data = request.data
        user_id = req_data.get('id')
        user = User.objects.get(pk=user_id)
        user.user_lock = False
        user.save()
        resp_data = {
            "status": status.HTTP_205_RESET_CONTENT,
            "msg": "Updated Ok",
            "data": UserSerializer(user).data
        }
        return Response(resp_data)

    def enable(self, request):
        req_data = request.data
        user_id = req_data.get('id')
        user = User.objects.get(pk=user_id)
        user.user_freeze = False
        user.save()
        resp_data = {
            "status": status.HTTP_205_RESET_CONTENT,
            "msg": "Updated Ok",
            "data": UserSerializer(user).data
        }
        return Response(resp_data)

    def disable(self, request):
        req_data = request.data
        user_id = req_data.get('id')
        user = User.objects.get(pk=user_id)
        user.user_freeze = True
        user.save()
        resp_data = {
            "status": status.HTTP_205_RESET_CONTENT,
            "msg": "Updated Ok",
            "data": UserSerializer(user).data
        }
        return Response(resp_data)


# system_notice
class ManageSystemNoticeAPIView(APIView):
    authentication_classes = [ManagerAuthentication, ]
    permission_classes = [ManagerLogin, ]

    def get(self, request):
        page_number = request.query_params.get("page_number")
        page_size = request.query_params.get("page_size")
        system_notices = SystemNotice.objects.all()
        notice_list = Paginator(system_notices, per_page=page_size)
        notices = notice_list.page(page_number)

        result = []
        for sn in notices:
            serizlizer = SystemNoticeSerializer(sn)
            result.append(serizlizer.data)
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Query Ok",
            "data": result,
            "total_number": notice_list.count,
            "total_page": notice_list.num_pages
        }

        return Response(resp_data)

    def post(self, request):
        req_data = request.data
        manager_token = request.query_params.get("token")
        manager_id = cache.get(manager_token)
        manager = Manager.objects.get(pk=manager_id)
        make_data = {
            "send_user": manager.id,
            "receive_group": req_data.get("receive_group"),
            "system_notice_default": req_data.get("system_notice_default"),
            "system_notice_topic": req_data.get("system_notice_topic"),
            "system_notice_content": req_data.get("system_notice_content")
        }
        serializer = SystemNoticeSerializer(data=make_data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            resp_data = {
                "status": status.HTTP_201_CREATED,
                "msg": "新建系统通知成功",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            return Response(req_data)

    def put(self, request):
        action = request.query_params.get("action")

        if action == "deactivate":
            return self.deactivate(request)
        elif action == "activate":
            return self.activate(request)
        else:
            return Response("暂不提供其他功能")

    def deactivate(self, request):
        notice_id = request.data.get("id")
        notice = SystemNotice.objects.get(pk=notice_id)
        notice.system_notice_activate = False
        notice.save()
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Update Ok",
            "data": SystemNoticeSerializer(notice).data
        }
        return Response(resp_data)

    def activate(self, request):
        notice_id = request.data.get("id")
        notice = SystemNotice.objects.get(pk=notice_id)
        notice.system_notice_activate = True
        notice.save()
        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "Update Ok",
            "data": SystemNoticeSerializer(notice).data
        }
        return Response(resp_data)

    def delete(self, request):
        notice_id = request.data.get("id")
        system_notice = SystemNotice.objects.get(pk=notice_id)
        serializer = SystemNoticeSerializer(system_notice)
        if system_notice.delete():
            resp_data = {
                "status": status.HTTP_200_OK,
                "msg": "Deleted",
                "data": serializer.data
            }
            return Response(resp_data)
        else:
            return Response("Failed")
