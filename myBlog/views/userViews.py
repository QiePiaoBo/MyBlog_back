from django.core.cache import cache
from django.shortcuts import render

# Create your views here.


# 管理员登录

from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed, PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.cache_timeout_util import USER_TIMEOUT, MANAGER_TIMEOUT
from common.utils.token_util import generate_user_token, generate_manager_token
from common.utils.user_grade import get_grade
from myBlog.authentications.user_authentication import UserAuthentication
from myBlog.models import Manager, User, Attention, UserMood, Theme, SecretMessage, Stay
from myBlog.permissions.user_permission import UserLogin
from myBlog.serializers.relationSerializer import AttentionSerializer, SecretMessageSerializer, StaySerializer
from myBlog.serializers.userSerializer import ManagerSerializer, UserSerializer, UserMoodSerializer, ThemeSerializer


# 管理员登录

class ManagerUserAPIView(CreateAPIView):
    serializer_class = ManagerSerializer

    def post(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        if action == 'register':
            resp_data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "您没有权限新建管理员"
            }

            return Response(resp_data)
        elif action == 'login':
            return self.do_login(request, *args, **kwargs)
        else:
            resp_data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "您没有权限做其他操作"
            }
            return Response(resp_data)

    def do_login(self, request, *args, **kwargs):

        manager_account = request.data.get("manager")

        manager_password = request.data.get("manager_password")

        try:
            if Manager.objects.get(manager_name=manager_account):
                user = Manager.objects.get(manager_name=manager_account)
            else:
                user = Manager.objects.get(manager_phone=manager_account)

        except Manager.DoesNotExist:
            raise NotFound(detail="用户不存在")

        if not user.verify_password(manager_password):
            raise AuthenticationFailed(detail="密码错误")

        token = generate_manager_token()
        cache.set("token", token, timeout=MANAGER_TIMEOUT)
        cache.set(token, user.id, timeout=MANAGER_TIMEOUT)

        resp_user = {
            "id": user.id,
            "name": user.manager_name,
            "phone": user.manager_phone
        }

        resp_data = {
            "status": status.HTTP_200_OK,
            "info": resp_user,
            "msg": "登录成功",
            "token": token
        }

        return Response(resp_data)


# 用户登录注册
class UserAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        if action == "register":
            return self.do_register(request, *args, **kwargs)
        elif action == "login":
            return self.do_login(request, *args, **kwargs)
        # elif action == "logout":
        #     return self.do_logout(request, *args, **kwargs)
        else:
            return ValidationError(detail="参数错误,登录或注册")

    def do_register(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not serializer.save():
            data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "xinxichongfu",
                "data": request.data
            }
            return data
        # 在新用户注册成功的时候,同时添加theme表中的记录
        user_name = request.data.get("user_name")
        user = User.objects.get(user_name=user_name)
        user_id = user.id

        theme = {
            "user_id":user_id,
            "recent_theme": 1,
            "fav_theme": 2
        }
        theme_serializer = ThemeSerializer(data=theme)
        theme_serializer.is_valid(raise_exception=True)
        theme_serializer.save()

        headers = self.get_success_headers(serializer.data)

        resp_data = {
            "status": status.HTTP_201_CREATED,
            "msg": "创建成功",
            "data": request.data
        }

        return Response(resp_data, headers=headers)

    def do_login(self, request, *args, **kwargs):

        user_account = request.data.get("user")
        user_password = request.data.get("user_password")
        way = request.data.get("way")

        try:
            if way == "phone":
                user = User.objects.get(user_phone=user_account)
            elif way == "name":
                user = User.objects.get(user_name=user_account)
            elif way == "email":
                user = User.objects.get(user_email=user_account)
            else:
                raise NotFound(detail="您所输入的用户不存在")
        except User.DoesNotExist:
            data = {
                "status": status.HTTP_404_NOT_FOUND,
                "msg": "您输入的用户不存在",
                "data": request.data
            }
            return Response(data)

        # try:
        #     if User.objects.get(user_name=user_account):
        #         user = User.objects.get(user_name=user_account)
        #     elif User.objects.get(user_phone=user_account):
        #         user = User.objects.get(user_phone=user_account)
        #     else:
        #         user = None
        # except User.DoesNotExist:
        #     raise NotFound(detail="用户不存在")

        if not user.verify_password(user_password):
            data = {
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "msg": "密码错误",
                "data": request.data
            }
            return Response(data)

        if user.user_lock:
            data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "用户已被禁用",
                "data": request.data
            }
            return Response(data)
        # print("2@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        token = generate_user_token()

        cache.set("token", token, timeout=USER_TIMEOUT)
        cache.set(token, user.id, timeout=USER_TIMEOUT)

        resp_user = {
            "id": user.id,
            "name": user.user_name,
            "phone": user.user_phone,
            "token": token
        }

        resp_data = {
            "status": status.HTTP_200_OK,
            "msg": "登录成功",
            "data": resp_user
        }

        return Response(resp_data)


# 用户关注用户
class UserAttentionAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        print(user_id)

        attentions = Attention.objects.filter(user_id=user_id)
        # print(attentions.count())
        #
        users = []
        for attention in attentions:
            user_id = attention.attention_id.id
            user_name = attention.attention_id.user_name

            user = {
                "user_id": user_id,
                "user_name": user_name
            }
            users.append(user)

        data = {
            "users": users
        }

        return Response(data)

    def post(self, request, *args, **kwargs):

        user_id = request.data.get("user_id")

        serializer = AttentionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        group = get_grade(user_id)

        # 为了测试方便 部署时应该去掉等于号
        # 只有当用户的组是2以及更高时,才能关注
        if group.id >= 1:
            serializer.save()
            data = {
                "status": status.HTTP_201_CREATED,
                "msg": "关注成功",
                "data": serializer.data
            }
        else:
            data = {
                "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                "msg": "请您完善信息后再关注噢.",
                "data": serializer.data
            }

        return Response(data)

    def delete(self, request, *args, **kwargs):
        serializer = AttentionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.delete(serializer)
        data = {
            "status": status.HTTP_200_OK,
            "msg": "取关成功",
            "data": serializer.delete(serializer)
        }
        return Response(data)


# 用户心情
class UserMoodAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    def get(self, request):
        user_id = cache.get(request.query_params.get('token'))
        moods = UserMood.objects.filter(user_id=user_id)

        res = []
        for mood in moods:
            serializer = UserMoodSerializer(mood)
            res.append(serializer.data)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "获取成功",
            "data": res
        }

        return Response(data)

    def post(self, request):

        user_id = cache.get(request.query_params.get('token'))

        # print(cache.get(request.query_params.get('token')))

        print(request.META['REMOTE_ADDR'])

        serializer = UserMoodSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # if get_grade(user_id).id > 2:
        if get_grade(user_id).id >= 1:
            serializer.save()

            data = {
                "status": status.HTTP_201_CREATED,
                "msg": "发表心情成功",
                "data": serializer.data
            }
        else:
            data = {
                "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                "msg": "现在还不行噢小弟弟",
                "data": serializer.data
            }
        return Response(data)

    def delete(self, request):

        user_id = cache.get(request.query_params.get('token'))
        mood_id = request.data.get('mood_id')

        user = User.objects.get(pk=user_id)
        mood = UserMood.objects.get(pk=mood_id)
        if mood.user_id == user:
            serializer = UserMoodSerializer(mood)
            serializer.delete(mood_id)

            data = {
                "status": status.HTTP_200_OK,
                "msg": "删除成功",
                "data": serializer.data
            }

            return Response(data)
        else:
            return Response("您不能删除其他人的心情")

    def put(self, request, *args, **kwargs):

        user_id = cache.get(request.query_params.get('token'))
        # print(user_id)
        mood_id = request.data.get('mood_id')

        user = User.objects.get(pk=user_id)
        try:
            mood = UserMood.objects.get(pk=mood_id)
            if mood.user_id == user:
                serializer = UserMoodSerializer(data=request.data)

                serializer.is_valid(raise_exception=True)

                serializer.update(mood, serializer.validated_data)

                data = {
                    "status": status.HTTP_200_OK,
                    "msg": "更新成功",
                    "data": serializer.data
                }

                return Response(data)

            else:
                data = {
                    "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    "msg": "您不能修改别人的心情",
                    "data": request.data
                }

                return Response(data)
        except UserMood.DoesNotExist:
            raise NotFound("未找到您想要修改的心情")


# 用户主题
class UserThemeAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    def get(self, request):
        user_id = cache.get(request.query_params.get('token'))
        theme = Theme.objects.get(user_id=user_id)

        serializer = ThemeSerializer(theme)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "It is OK",
            "data": serializer.data
        }
        return Response(data)

    def post(self, request):

        req_data = request.data

        #  根据token确定用户,拼接真实请求结果
        user_id = cache.get(request.query_params.get('token'))

        serializer = ThemeSerializer(data=req_data)

        if int(request.data.get('user_id')) == user_id:

            serializer.is_valid(raise_exception=True)

            if serializer.save():

                data = {
                    "status": status.HTTP_201_CREATED,
                    "msg": "接头成功,无内鬼",
                    "data": request.data
                }
            else:
                data = {
                    "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    "msg": "该用户的主题已经创建过",
                    "data": request.data
                }
        else:
            data = {
                "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                "msg": "No Permission To Change Others Theme.",
                "data": request.data
            }

        return Response(data)

    def put(self, request):

        user_id = cache.get(request.query_params.get('token'))
        user = User.objects.get(pk=user_id)
        theme = Theme.objects.get(user_id=user)

        print(theme.recent_theme)

        serizlizer = ThemeSerializer(data=request.data)
        serizlizer.is_valid(raise_exception=True)
        serizlizer.update(theme, serizlizer.validated_data)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "更新成功",
            "data": serizlizer.validated_data
        }

        return Response(data)


# 用户私信
class UserSecretMessageAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    # 用户获取自己接受的私信
    def get(self, request):
        user_id = cache.get(request.query_params.get('token'))
        user = User.objects.get(pk=user_id)
        secret_messages = SecretMessage.objects.filter(receive_id=user)

        list = []
        for secret_message in secret_messages:
            serializer = SecretMessageSerializer(secret_message)
            list.append(serializer.data)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "Query OK",
            "data": list
        }

        return Response(data)

    # 用户发送私信
    def post(self, request):
        user_id = cache.get(request.query_params.get('token'))
        req_data = request.data
        user = User.objects.get(pk=user_id)

        serializer = SecretMessageSerializer(data=req_data)

        if int(request.data.get('send_id')) == user_id:

            serializer.is_valid(raise_exception=True)

            if serializer.save():

                data = {
                    "status": status.HTTP_201_CREATED,
                    "msg": "接头成功,无内鬼",
                    "data": request.data
                }
            else:
                data = {
                    "status": status.HTTP_204_NO_CONTENT,
                    "msg": "私信发送失败",
                    "data": request.data
                }
        else:
            data = {
                "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                "msg": "亲,表白要勇敢噢",
                "data": request.data
            }

        return Response(data)

    # 用户更改私信状态(是否已读)
    def put(self, request):

        user_id = cache.get(request.query_params.get('token'))

        secret_id = request.data.get("secret_message_id")
        secret_message = SecretMessage.objects.get(pk=secret_id)

        serializer = SecretMessageSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.update(secret_message, serializer.validated_data)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "状态已经更新为已读",
            "data": serializer.validated_data
        }
        return Response(data)


# 用户留言
class StaySaidAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    # 获取当前用户接收的的留言
    def get(self, request):
        user_id = cache.get(request.query_params.get('token'))
        user = User.objects.get(pk=user_id)

        stay_saids = Stay.objects.filter(user_id=user)

        list = []
        for stay_said in stay_saids:
            serializer = StaySerializer(stay_said)
            list.append(serializer.data)

        data = {
            "status": status.HTTP_200_OK,
            "msg": "获取成功",
            "data": list
        }
        return Response(data)

    # 添加留言
    def post(self, request):
        user_id = cache.get(request.query_params.get('token'))

        req_data = request.data

        register_ip = request.META['REMOTE_ADDR']
        serializer = StaySerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        if int(serializer.validated_data.get("stay_user_id")) == user_id:
            serializer.save()
            data = {
                "status": status.HTTP_201_CREATED,
                "msg": "添加成功",
                "data": req_data
            }
        else:
            data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "留言要用自己的名字噢",
                "data": req_data
            }
        return Response(data)


# 首页用户
class IndexUsersAPIView(APIView):

    def get(self, request):
        users = User.objects.filter(user_lock=0)
        res_users = []
        for user in users:
            serializer = UserSerializer(user)
            user_sex = "man"
            if serializer.data.get('user_sex'):
                user_sex = "man"
            elif not serializer.data.get('user_sex'):
                user_sex = "woman"
            piece_data = {
                "id": serializer.data.get('id'),
                "user_name": serializer.data.get('user_name'),
                "user_sex": user_sex,
                "user_address": serializer.data.get('user_address'),
                "icon": serializer.data.get('user_image_url'),
            }
            res_users.append(piece_data)
        res_data = {
            "status": 200,
            "msg": "Query Ok",
            "data": res_users
        }
        return Response(res_data)


# 用户信息
class InfoUserAPIView(APIView):

    def get(self, request):
        user_name = request.query_params.get('user_name')
        user_id = request.query_params.get('user_id')
        user = None
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            if user_name:
                user = User.objects.get(user_name=user_name)
            else:
                return Response("Infomation not enough")

        serializer = UserSerializer(user)
        res_user = serializer.data
        result_data = {
            "user_id": res_user.get('id'),
            "user_name": res_user.get('user_name'),
            "user_sex": res_user.get("user_sex"),
            "user_address": res_user.get("user_address"),
            "user_mark": res_user.get("user_mark"),
            "user_birthday": res_user.get("user_birthday"),
            "user_school": res_user.get("user_school"),
            "user_description": res_user.get("user_description"),
            "user_weibo": res_user.get("user_weibo"),
            "user_blood": res_user.get("user_blood"),
            "user_says": res_user.get("user_says"),
        }
        return Response(result_data)


