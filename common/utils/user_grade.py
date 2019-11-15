from myBlog.models import User


def get_grade(user_id):

    user = User.objects.get(pk=user_id)

    return user.group_id






