import math

from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myBlog.authentications.user_authentication import UserAuthentication
from myBlog.models import Blog, User, Commit, Article
from myBlog.permissions.user_permission import UserLogin
from myBlog.serializers.blogSerializer import BlogSerializer, ArticleSerializer
from myBlog.serializers.relationSerializer import CommitSerializer


# 点赞
class AggrementAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    # 点赞
    def put(self, request):
        blog_id = request.data.get("blog_id")
        attitude = request.data.get("attitude")

        blog = Blog.objects.get(pk=blog_id)

        serializer = BlogSerializer(blog)

        agree = serializer.data.get("blog_agree")

        disagree = serializer.data.get("blog_disagree")
        if attitude == "agree":
            update_data = {
                "blog_id": blog_id,
                "blog_agree": agree + 1
            }
        elif attitude == "disagree":
            update_data = {
                "blog_id": blog_id,
                "blog_disagree": disagree + 1
            }
        update = BlogSerializer(data=update_data)
        update.is_valid(raise_exception=True)

        update.update(blog, update_data)

        return Response(update.validated_data)


# 用户评论
class CommitAPIView(APIView):

    # 根据文章id,文章作者,评论者来获取评论记录
    def post(self, request):
        way = request.query_params.get("way")
        if way:
            return self.do_search(request)
        else:
            return self.do_commit(request)

    def do_search(self, request):
        way = request.query_params.get("way")
        commits = None
        if way == "article":
            commits = Commit.objects.filter(committed_blog=request.data.get("blog_id"))
        elif way == "author":
            commits = Commit.objects.filter(author=request.data.get("author"))
        elif way == "user":
            user_id = cache.get(request.query_params.get("token"))
            commits = Commit.objects.filter(committer=user_id)
        elif way == "all":
            commits = Commit.objects.all()
        elif way == None:
            self.do_commit(request)
        commit_list = []
        for commit in commits:
            serializer = CommitSerializer(commit)
            committer_id = serializer.data.get("committer")
            committer_name = User.objects.get(pk=committer_id).user_name
            commit_data = {
                "id": serializer.data.get("id"),
                "committer": committer_name,
                "commit_star": serializer.data.get('commit_stars'),
                "commit_content": serializer.data.get('commit_content'),
                "commit_time": serializer.data.get('commit_time')
            }
            commit_list.append(commit_data)
        data = {
            "status": status.HTTP_200_OK,
            "msg": "Query Ok",
            "data": commit_list
        }
        return Response(data)

    def do_commit(self, request):
        if not request.query_params.get('token'):
            return Response("身份认证信息未提供")
        elif not cache.get(request.query_params.get('token')):
            return Response("身份认证信息未提供")
        serializer = CommitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.complete_save(serializer)
        data = {
            "status": status.HTTP_201_CREATED,
            "msg": "created",
            "data": serializer.data
        }
        return Response(data)

    def delete(self, request):
        if not request.query_params.get('token'):
            return Response("身份认证信息未提供")
        elif not cache.get(request.query_params.get('token')):
            return Response("身份认证信息未提供")

        user_id = cache.get(request.query_params.get("token"))

        commit_id = request.data.get('commit_id')

        commit = Commit.objects.get(pk=commit_id)

        serializer = CommitSerializer(commit)

        if commit.committer.id == user_id:

            commit.delete()
            data = {
                "status": status.HTTP_200_OK,
                "msg": "Ok",
                "data": serializer.data
            }
        else:

            data = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "Don't do that please",
                "data": request.data
            }
        return Response(data)


# 文章
class ArticleAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    def get(self, request):
        user_id = cache.get(request.query_params.get("token"))
        user = User.objects.get(pk=user_id)

        articles = Article.objects.filter(article_author=user).filter(article_bloged=False)
        serializer = ArticleSerializer(articles, many=True)
        data = {
            "status": 200,
            "msg": "Ok",
            "data": serializer.data
        }
        return Response(data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "msg": "OK",
            "status": 204,
            "data": serializer.data
        }
        return Response(data)

    def put(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article_id = request.data.get("article_id")
        print(article_id)

        article = Article.objects.get(pk=article_id)
        serializer.update(article, serializer.validated_data)
        res_serializer = ArticleSerializer(article)
        data = {
            "meg": "Ok",
            "status": 200,
            "data": res_serializer.data
        }
        return Response(data)

    def delete(self, request):
        user_id = cache.get(request.query_params.get("token"))
        user = User.objects.get(pk=user_id)
        article_id = request.data.get("article_id")
        article = Article.objects.get(pk=article_id)
        article.delete()
        res_serializer = ArticleSerializer(article)
        if article.article_author != user:
            data = {
                "msg": "Please delete your own article",
                "status": 403,
                "data": {
                    "user_id": user_id,
                    "article_id": article_id
                }
            }
            return Response(data)
        else:
            data = {
                "msg": "Ok",
                "status": 200,
                "data": res_serializer.data
            }
            return Response(data)


# 查一篇文章
class ArticleGetAPIView(APIView):

    def get(self, request, aid):
        user_id = 0
        if request.query_params.get('token'):
            user_id = cache.get(request.query_params.get('token'))
        article = Article.objects.get(pk=aid)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

        # if article.article_author.id == user_id:
        #     serializer = ArticleSerializer(article)
        #     return Response(serializer)
        # else:
        #     data = {
        #         "msg": "Secret",
        #         "status": 18,
        #         "data": "私密文章,访问拒绝"
        #     }
        #     return Response(data)


# 博客(logged_in)
class BlogAPIView(APIView):
    authentication_classes = [UserAuthentication, ]
    permission_classes = [UserLogin, ]

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "msg": "ok",
            "status": 204,
            "data": serializer.data
        }
        return Response(data)

    def get(self, request):
        user_id = cache.get(request.query_params.get("token"))
        user = User.objects.get(pk=user_id)

        blogs = Blog.objects.filter(blog_author=user)
        serializer = BlogSerializer(blogs, many=True)

        data = {
            "msg": "Query Ok",
            "status": 200,
            "data": serializer.data
        }
        return Response(data)

    def delete(self, request):
        blog_id = request.data.get("blog_id")
        blog = Blog.objects.get(pk=blog_id)
        serializer = BlogSerializer(blog)
        user_id = cache.get(request.query_params.get("token"))
        user = User.objects.get(pk=user_id)

        if blog.blog_user == user:

            blog.delete()
            data = {
                "msg": "deleted",
                "status": 200,
                "data": serializer.data
            }
        else:
            data = {
                "msg": "Forbidden",
                "status": 403,
                "data": request.data
            }
        return Response(data)


# 查一篇blog
class BlogGetAPIView(APIView):

    def get(self, request, bid):
        user_id = 0
        if request.query_params.get('token'):
            user_id = cache.get(request.query_params.get('token'))
        blog = Blog.objects.get(pk=bid)
        if blog.blog_secret == 1:
            print('wenzhangbugongkai')
            if blog.blog_author.id == user_id:
                serializer = BlogSerializer(blog)
                return Response(serializer.data)
            else:
                data = {
                    "msg": "Secret",
                    "status": 18,
                    "data": "私密文章,访问拒绝"
                }
                return Response(data)
        else:
            serializer = BlogSerializer(blog)
            return Response(serializer.data)


# 查询首页的博客
class BlogsGetAPIView(APIView):

    def get(self, request):

        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        start = page_number*page_size - page_size

        blogs = Blog.objects.filter(blog_secret=0).order_by('-id')[start:page_size]

        total_page = math.ceil(len(blogs)/page_size)
        total_num = len(blogs)
        serializer = BlogSerializer(blogs, many=True)
        res_data = []
        for i in serializer.data:
            print(i)
            piece_author = User.objects.get(pk=i['blog_author'])

            piece_data = {
                "id": i['id'],
                "blog_keyword": i['blog_keyword'],
                "blog_description": i['blog_description'],
                "blog_author": piece_author.user_name,
                "blog_agree": i['blog_agree'],
                "blog_disagree": i['blog_disagree'],
            }
            res_data.append(piece_data)
        data = {
            "status":200,
            "msg":"Query OK",
            "data": res_data,
            "total_number":total_num,
            "total_page":total_page
        }
        return Response(data)
