from django.db import models
from django.utils import timezone

from myBlog.models.userModel import User, UserGroup


# # 文章分类
# class ArticleType(models.Model):
#     type_name = models.CharField(max_length=32, null=True, unique=True)
#
#     class Meta:
#         app_label = 'myBlog'
#         db_table = 'blog_article_type'


# 博客模块
class BlogType(models.Model):
    icon = models.CharField(max_length=64, null=True)
    type_name = models.CharField(max_length=64, null=True)
    is_del = models.BooleanField(default=False)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_blog_type'


# 文章
class Article(models.Model):
    article_author = models.ForeignKey(User, related_name="article_author", null=True)
    article_time = models.DateTimeField(default=timezone.now)
    article_ip = models.CharField(max_length=32, null=True)
    article_click = models.IntegerField(default=5, null=True)
    article_title = models.CharField(max_length=128, null=True, default=True)
    article_content = models.TextField(null=True)
    # 文章置顶/
    article_bloged = models.BooleanField(default=False)
    #

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_article'


# 博客
class Blog(models.Model):
    blog_keyword = models.CharField(max_length=64, null=True)
    # blog私密程度
    blog_secret = models.IntegerField(default=0, null=True)
    blog_description = models.CharField(max_length=256, null=True)
    blog_author = models.ForeignKey(User, related_name='blog_user', null=True)
    blog_type = models.ForeignKey(BlogType, related_name='blog_type', null=True)
    blog_content = models.ForeignKey(Article, related_name='blog_article', null=True)
    blog_top = models.BooleanField(default=False)
    blog_agree = models.IntegerField(null=True, default=0)
    blog_disagree = models.IntegerField(null=True, default=0)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_blog'
