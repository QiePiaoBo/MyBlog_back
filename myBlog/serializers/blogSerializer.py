from rest_framework import serializers
from myBlog.models.blogModel import *


#
# # 文章分类序列化
# class ArticleTypeSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ArticleType
#         fields = ("id", "type_name")
#


# 博客模块序列化
class BlogTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogType
        fields = ("id", "icon", "type_name")


# 文章序列化
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "article_author", "article_ip",
                  "article_click"
                  , "article_title", "article_content"
                  , "article_bloged")


# 博客序列化
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("id", "blog_keyword","blog_secret", "blog_description", "blog_author","blog_top"
                  , "blog_type", "blog_content", "blog_agree", "blog_disagree")
