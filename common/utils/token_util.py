import uuid

MANAGER = "manager"

USER = "user"


def generate_token(prefix):

    token = prefix + uuid.uuid4().hex
    return token


def generate_manager_token():
    return generate_token(MANAGER)


def generate_user_token():
    return generate_token(USER)


