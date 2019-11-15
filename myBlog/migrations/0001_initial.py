# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-08-26 02:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_name', models.CharField(max_length=128, null=True)),
                ('article_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('article_ip', models.CharField(max_length=32, null=True)),
                ('article_click', models.IntegerField(default=5, null=True)),
                ('article_secret', models.IntegerField(default=1, null=True)),
                ('article_title', models.CharField(default=True, max_length=128, null=True)),
                ('article_content', models.TextField(null=True)),
                ('article_top', models.BooleanField(default=False)),
                ('article_suppose', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'blog_article',
            },
        ),
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=32, null=True, unique=True)),
            ],
            options={
                'db_table': 'blog_article_type',
            },
        ),
        migrations.CreateModel(
            name='Attention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'blog_attention',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_keyword', models.CharField(max_length=64, null=True)),
                ('blog_description', models.CharField(max_length=256, null=True)),
                ('blog_agree', models.IntegerField(null=True)),
                ('blog_disagree', models.IntegerField(null=True)),
                ('blog_content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_article', to='myBlog.Article')),
            ],
            options={
                'db_table': 'blog_blog',
            },
        ),
        migrations.CreateModel(
            name='BlogType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=64, null=True)),
            ],
            options={
                'db_table': 'blog_blog_type',
            },
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commit_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('commit_content', models.CharField(max_length=256, null=True)),
                ('committed_blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myBlog.Blog')),
            ],
            options={
                'db_table': 'blog_commit',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'blog_friend',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=32, null=True, unique=True)),
                ('manager_phone', models.CharField(max_length=255, null=True, unique=True)),
                ('manager_email', models.CharField(max_length=128, unique=True)),
                ('manager_password', models.CharField(max_length=256, null=True)),
            ],
            options={
                'db_table': 'blog_manager',
            },
        ),
        migrations.CreateModel(
            name='PowerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_num', models.IntegerField(null=True, unique=True)),
                ('power_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'blog_power',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_grade', models.IntegerField(null=True, unique=True)),
                ('rank_mark', models.IntegerField(null=True, unique=True)),
                ('rank_name', models.CharField(max_length=128, null=True, unique=True)),
            ],
            options={
                'db_table': 'blog_rank',
            },
        ),
        migrations.CreateModel(
            name='SecretMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_topic', models.CharField(max_length=128, null=True)),
                ('message_content', models.CharField(max_length=256, null=True)),
                ('message_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'blog_secret_message',
            },
        ),
        migrations.CreateModel(
            name='Stay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.CharField(max_length=256, null=True)),
                ('stay_user_ip', models.CharField(max_length=32, null=True)),
                ('message_stay_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('place', models.CharField(max_length=128, null=True)),
            ],
            options={
                'db_table': 'blog_stay_said',
            },
        ),
        migrations.CreateModel(
            name='SystemNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_default', models.CharField(default='系统通知:', max_length=256)),
                ('system_topic', models.CharField(max_length=128, null=True)),
                ('system_content', models.CharField(max_length=256, null=True)),
            ],
            options={
                'db_table': 'blog_system_notice',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_theme', models.IntegerField(default=0, null=True)),
                ('recent_theme', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'blog_user_theme',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=128, null=True, unique=True)),
                ('user_password', models.CharField(max_length=255, null=True)),
                ('user_phone', models.CharField(max_length=255, null=True, unique=True)),
                ('user_sex', models.BooleanField(default=True)),
                ('user_qq', models.CharField(max_length=255, unique=True)),
                ('user_email', models.CharField(max_length=128, null=True, unique=True)),
                ('user_address', models.CharField(default='台湾省', max_length=255)),
                ('user_mark', models.IntegerField(default=100)),
                ('user_birthday', models.DateField(default='1997-4-13', null=True)),
                ('user_description', models.CharField(default='我是新人,大家快来欺负我', max_length=255, null=True)),
                ('user_image_url', models.CharField(default='https://img2.woyaogexing.com/2019/06/20/56e5b0d9b83a4370b188a3d2ed3571c3!400x400.webp', max_length=255, null=True)),
                ('user_school', models.CharField(default='青岛大学', max_length=128)),
                ('user_register_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_register_ip', models.CharField(max_length=128, null=True)),
                ('user_last_update_time', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('user_weibo', models.CharField(default='myblog@sina.com', max_length=128, null=True)),
                ('user_blood', models.CharField(default='O型血', max_length=16)),
                ('user_says', models.CharField(default='当我站在高处,却发现自己总是孤独,当一阵逆风袭来,我已能抵御八面来风', max_length=255, null=True)),
                ('user_lock', models.BooleanField(default=False)),
                ('user_freeze', models.BooleanField(default=False)),
                ('user_power', models.CharField(default='1,2,3', max_length=255)),
            ],
            options={
                'db_table': 'blog_user',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_num', models.IntegerField(null=True, unique=True)),
                ('group_name', models.CharField(default='膝盖中箭组', max_length=255, null=True, unique=True)),
                ('group_power', models.CharField(default='1,2,3', max_length=255)),
            ],
            options={
                'db_table': 'blog_user_group',
            },
        ),
        migrations.CreateModel(
            name='UserMood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood_time', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('mood_ip', models.CharField(max_length=64, null=True)),
                ('mood_content', models.CharField(max_length=256, null=True)),
                ('type_id', models.CharField(default='早晨起来拥抱太阳', max_length=128, null=True)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Mood_user', to='myBlog.User')),
            ],
            options={
                'db_table': 'blog_user_mood',
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('visitor_ip', models.CharField(max_length=64, null=True)),
                ('type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Visitor_article_type', to='myBlog.ArticleType')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Visitor_visited', to='myBlog.User')),
                ('visitor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Visitor_visitor', to='myBlog.User')),
            ],
            options={
                'db_table': 'blog_visitor',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='group_id',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='myBlog.UserGroup'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_rank_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myBlog.Rank'),
        ),
        migrations.AddField(
            model_name='theme',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Theme_user', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='systemnotice',
            name='send_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myBlog.UserGroup'),
        ),
        migrations.AddField(
            model_name='systemnotice',
            name='send_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='stay',
            name='stay_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stay_user_id', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='stay',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='secretmessage',
            name='receive_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Secret_receive', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='secretmessage',
            name='send_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Secret_send', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Friend_friend', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='friend',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Friend_user', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='commit',
            name='committed_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commit_commited', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='commit',
            name='type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Commit_article_type', to='myBlog.ArticleType'),
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_type', to='myBlog.BlogType'),
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_user', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='attention',
            name='attention_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Attention_attention', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='attention',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Attention_user', to='myBlog.User'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_blog_type',
            field=models.ForeignKey(default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='myBlog.BlogType'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_type', to='myBlog.ArticleType'),
        ),
    ]
