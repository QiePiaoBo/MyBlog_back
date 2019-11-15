from django.conf.urls import url

from myBlog.views import userViews, blogViews, relationViews

urlpatterns = [
    url(r'^manager/', userViews.ManagerUserAPIView().as_view()),
    url(r'^user/', userViews.UserAPIView().as_view()),
    url(r'^attention/', userViews.UserAttentionAPIView().as_view()),
    url(r'^mood/', userViews.UserMoodAPIView().as_view()),
    url(r'^theme/', userViews.UserThemeAPIView().as_view()),
    url(r'^secret/', userViews.UserSecretMessageAPIView().as_view()),
    url(r'^stay/', userViews.StaySaidAPIView().as_view()),
    url(r'^agreement/',blogViews.AggrementAPIView().as_view()),
    url(r'^commit/',blogViews.CommitAPIView().as_view()),
    url(r'^articles/',blogViews.ArticleAPIView().as_view()),
    url(r'^article/(?P<aid>\d+)/$',blogViews.ArticleGetAPIView().as_view()),
    url(r'^blogs/',blogViews.BlogAPIView().as_view()),
    url(r'^blog/(?P<bid>\d+)/$',blogViews.BlogGetAPIView().as_view()),
    url(r'^index_blog/',blogViews.BlogsGetAPIView().as_view()),
    url(r'^marks/',relationViews.MarkAPIView.as_view()),
]
