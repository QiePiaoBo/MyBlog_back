from rest_framework import serializers
from myBlog.models.userModel import *
from django.utils import timezone

# 管理员序列化
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ("id", "manager_name", "manager_phone", "manager_email", "manager_password")


# 权限表序列化
class PowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerList
        fields = ("id", "power_num", "power_name")


# 用户组序列化
class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ("id", "group_num", "group_name", "group_power")


# 用户等级序列化
class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ("id", "rank_grade", "rank_mark", "rank_name")


# 用户序列化
class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User()
        group = UserGroup.objects.get(pk=1)
        user.group_id = group
        user.user_name = validated_data.get("user_name")
        user.user_phone = validated_data.get("user_phone")
        user.user_sex = False
        user.user_qq = validated_data.get("user_qq")
        user.user_email = validated_data.get("user_email")
        user.user_address = validated_data.get("user_address")
        user.user_mark = 100
        user.user_rank_id = validated_data.get("user_rank_id")
        user.user_birthday = validated_data.get("user_birthday")
        user.user_description = "已有的事,后必再有;已行的事,后必再行"
        user.user_image_url = "https://img2.woyaogexing.com/2019/06/20/56e5b0d9b83a4370b188a3d2ed3571c3!400x400.webp"
        user.user_school = "青岛大学"
        user.user_register_time = timezone.now()
        user.user_register_ip = validated_data.get("user_register_ip")
        user.user_last_update_time = timezone.now()
        user.user_weibo = "myblog@sina.com"
        user.user_blood = "O型血"
        user.user_says = "当我站在高处,却发现自己总是孤独"
        user.user_lock = False
        user.user_freeze = True
        user.set_password(validated_data.get("user_password"))
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "group_id", "user_name", "user_password", "user_phone", "user_sex",
                  "user_qq", "user_email", "user_address", "user_mark", "user_rank_id", "user_birthday",
                  "user_description", "user_image_url", "user_school", "user_register_time", "user_register_ip",
                  "user_last_update_time", "user_weibo", "user_blood", "user_says", "user_lock", "user_freeze")


# 用户心情序列化
class UserMoodSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        mood = UserMood()
        mood.user_id = validated_data.get("user_id")
        mood.mood_time = timezone.now()
        mood.mood_ip = validated_data.get('mood_ip')
        mood.mood_content = validated_data.get('mood_content')
        mood.mood_title = validated_data.get('mood_title')
        mood.mood_secret = validated_data.get('mood_secret')

        mood.save()
        return mood

    def delete(self,id):
        mood = UserMood.objects.get(pk=id)

        mood.delete()
        return mood

    class Meta:
        model = UserMood
        fields = ("id", "user_id", "mood_time", "mood_ip", "mood_content", "mood_title", "mood_secret")


# 用户主题序列化
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "user_id", "fav_theme", "recent_theme")
