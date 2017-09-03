import uuid

from flask import session
from models.user import User


def current_user():
    user_id = session.get('user_id', None)
    if user_id is not None:
        u = User.find(user_id)
        return u
    else:
        return None


csrf_tokens = {}


def new_csrf_token():
    u = current_user()
    if u is not None:
        token = str(uuid.uuid4())
        csrf_tokens[token] = u.id
    else:
        token = -100
    print(csrf_tokens)
    return token
