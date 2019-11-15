from rest_framework import serializers
from myBlog.models.relationModel import *


# 好友序列化
class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ("id", "user_id", "friend_id")


# 关注表序列化
class AttentionSerializer(serializers.ModelSerializer):

    def delete(self, validated_data):
        user_id = validated_data.data.get('user_id')
        attention_id = validated_data.data.get('attention_id')
        attention = Attention.objects.filter(user_id=user_id).filter(attention_id=attention_id)

        attention.delete()
        return attention

    class Meta:
        model = Attention
        fields = ("id", "user_id", "attention_id")


# 私信表序列化
class SecretMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretMessage
        fields = ("id", "send_id", "receive_id", "message_topic",
                  "message_content", "message_time", "is_read")


# 系统通知表序列化
class SystemNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemNotice
        fields = ("id", "send_id", "send_group_id", "send_default",
                  "system_topic", "system_content")


# 留言表序列化
class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = ("id", "user_id", "stay_user_id", "message_content"
                  , "stay_user_ip", "message_stay_time", "place")


# 访客序列化
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ("id", "visitor_id", "user_id", "visit_time"
                  , "visitor_ip", "type_id")


# 评论序列化
class CommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commit
        fields = ("id", "committer", "commit_time",
                  "committed_blog", "commit_content", "commit_stars")


# 收藏请求序列化
class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ("id", "user_id", "fav_blog")


