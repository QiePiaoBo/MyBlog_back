from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone
# Create your models here.

# 管理员



class Manager(models.Model):
    manager_name = models.CharField(max_length=32, unique=True, null=True)
    manager_phone = models.CharField(max_length=255, unique=True, null=True)
    manager_email = models.CharField(max_length=128, unique=True)
    manager_password = models.CharField(max_length=256, null=True)

    # 设置密码
    def set_password(self, password):
        self.manager_password = make_password(password)

    #     验证密码
    def verify_password(self, password):
        return check_password(password, self.manager_password)

    class Meta:
        app_label = 'myBlog'
        db_table = 'blog_manager'


# 权限表
class PowerList(models.Model):
    power_num = models.IntegerField(unique=True, null=True)
    power_name = models.CharField(max_length=128)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_power"


# ----------------------获取第一个用户组作为用户的默认外键取值
# def get_group():
#     return UserGroup.objects.get_or_create(id=1)[0].id


# 用户组
class UserGroup(models.Model):
    group_num = models.IntegerField(null=True, unique=True)
    group_name = models.CharField(null=True, unique=True, default="膝盖中箭组", max_length=255)
    group_power = models.CharField(max_length=255, default='1,2,3')

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_user_group"


# 用户等级
class Rank(models.Model):
    rank_grade = models.IntegerField(null=True, unique=True)
    rank_mark = models.IntegerField(unique=True, null=True)
    rank_name = models.CharField(max_length=128, unique=True, null=True)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_rank"


# 用户
class User(models.Model):
    group_id = models.ForeignKey(UserGroup, null=True, default=1)
    user_name = models.CharField(max_length=128, unique=True, null=True)
    user_password = models.CharField(max_length=255, null=True)
    user_phone = models.CharField(max_length=255, unique=True, null=True)
    user_sex = models.BooleanField(default=True)
    user_qq = models.CharField(max_length=255, unique=True,null=True)
    user_email = models.CharField(max_length=128, unique=True, null=True)
    user_address = models.CharField(max_length=255, default="台湾省")
    user_mark = models.IntegerField(default=100)
    user_rank_id = models.ForeignKey(Rank, null=True)
    user_birthday = models.DateField(default='1997-4-13', null=True)
    user_description = models.CharField(max_length=255, default='我是新人,大家快来欺负我', null=True)
    user_image_url = models.CharField(max_length=255,
                                      default='https://img2.woyaogexing.com/2019/06/20/56e5b0d9b83a4370b188a3d2ed3571c3!400x400.webp',
                                      null=True)
    user_school = models.CharField(max_length=128, default="青岛大学")
    user_register_time = models.DateTimeField(auto_now_add=True, null=True)
    user_register_ip = models.CharField(max_length=128, null=True)
    user_last_update_time = models.DateTimeField(default=timezone.now, null=True)
    user_weibo = models.CharField(max_length=128, default="myblog@sina.com", null=True)
    user_blood = models.CharField(max_length=16, default="O型血")
    user_says = models.CharField(max_length=255, default="当我站在高处,却发现自己总是孤独,当一阵逆风袭来,我已能抵御八面来风", null=True)
    user_lock = models.BooleanField(default=False)
    user_freeze = models.BooleanField(default=False)

    # user_power = models.CharField(max_length=255, default="1,2,3")

    # 设置密码
    def set_password(self, password):
        self.user_password = make_password(password)

    #     验证密码
    def verify_password(self, password):
        return check_password(password, self.user_password)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_user"


# 用户心情说说表
class UserMood(models.Model):
    user_id = models.ForeignKey(User, related_name='Mood_user', null=True)
    mood_time = models.DateTimeField(default=timezone.now, null=True)
    mood_ip = models.CharField(max_length=64, null=True)
    mood_content = models.TextField(null=True, default="早晨起来拥抱太阳")
    mood_title = models.CharField(max_length=128, null=True)
    mood_secret = models.BooleanField(default=False)

    class Meta:
        app_label = 'myBlog'
        db_table = "blog_user_mood"


# 偏爱主题
class Theme(models.Model):
    user_id = models.OneToOneField(User, related_name='Theme_user', null=True, unique=True,on_delete=models.CASCADE)
    fav_theme = models.IntegerField(default=0, null=True)
    recent_theme = models.IntegerField(null=True)

    class Meta:
        app_label = "myBlog"
        db_table = "blog_user_theme"









