from django.db import models
from django.utils import timezone

from myBlog.models.blogModel import Blog, BlogType
from myBlog.models.userModel import User, UserGroup, Manager


# 好友表
class Friend(models.Model):
    user_id = models.ForeignKey(User, related_name='Friend_user', null=True)
    friend_id = models.ForeignKey(User, related_name='Friend_friend', null=True)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_friend'


# 关注表
class Attention(models.Model):
    user_id = models.ForeignKey(User, related_name='Attention_user', null=True)
    attention_id = models.ForeignKey(User, related_name='Attention_attention', null=True)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_attention'


# 私信表
class SecretMessage(models.Model):
    send_id = models.ForeignKey(User, related_name='Secret_send', null=True)
    receive_id = models.ForeignKey(User, related_name='Secret_receive', null=True)
    message_topic = models.CharField(max_length=128, null=True)
    message_content = models.CharField(max_length=256, null=True)
    message_time = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_secret_message'


# 系统通知表
class SystemNotice(models.Model):
    # 发送者
    send_user = models.ForeignKey(Manager, related_name="发送者",null=True)
    # 接受组
    receive_group = models.ForeignKey(UserGroup, related_name="接受组",null=True)
    # 默认发送内容
    system_notice_default = models.CharField(max_length=256, default='系统通知:')
    system_notice_topic = models.CharField(max_length=128, null=True)
    system_notice_content = models.CharField(max_length=256, null=True)
    system_notice_activate = models.BooleanField(default=False)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_system_notice'


# 留言表
class Stay(models.Model):
    user_id = models.ForeignKey(User, null=True)
    stay_user_id = models.ForeignKey(User, related_name='stay_user_id')
    message_content = models.CharField(max_length=256, null=True)
    stay_user_ip = models.CharField(max_length=32, null=True)
    message_stay_time = models.DateTimeField(default=timezone.now)
    place = models.CharField(max_length=128, null=True)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_stay_said"


# 访客
class Visitor(models.Model):
    visitor_id = models.ForeignKey(User, related_name='Visitor_visitor', null=True)
    user_id = models.ForeignKey(User, related_name='Visitor_visited', null=True)
    visit_time = models.DateTimeField(default=timezone.now)
    visitor_ip = models.CharField(max_length=64, null=True)
    # 访问的板块
    type_id = models.ForeignKey(BlogType, related_name='Visitor_blog_type', null=True)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_visitor"


# 评论表
class Commit(models.Model):
    committer = models.ForeignKey(User, related_name='commit_commit', null=True)
    commit_time = models.DateTimeField(default=timezone.now)
    committed_blog = models.ForeignKey(Blog, null=True)
    commit_content = models.CharField(max_length=256, null=True)
    commit_stars = models.IntegerField(null=True, default=0)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_commit"


# 收藏
class Mark(models.Model):
    user_id = models.ForeignKey(User, null=True)
    fav_blog = models.ForeignKey(Blog, null=True)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_mark"
