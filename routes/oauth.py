import requests

from config import weibo_oauth
from models.user import User


def get_access_token(data):
    # return access_token, dict
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    r = requests.post(access_token_url, data=data)
    return r.json()


def user_info_from_service(access_tokens):
    # return user_info, dict
    access_token = access_tokens.get('access_token')
    uid = access_tokens.get('uid')
    info_url = 'https://api.weibo.com/2/users/show.json?access_token={}&uid={}'.format(access_token, uid)
    form = requests.get(info_url).json()
    user_info = {}
    user_info['username'] = form['name']
    user_info['password'] = '123456'
    user_info['user_image'] = form['profile_image_url']
    user_info['signature'] = form['description']
    return user_info


def user_from_oauth(code):
    data = weibo_oauth.copy()
    data['code'] = code
    # get access_tokens
    access_tokens = get_access_token(data)
    # get user_info
    user_info = user_info_from_service(access_tokens)

    u = User.find_by(username=user_info['username'])
    if u is None:
        # register a new user
        User.validate_register(user_info)
        u = User.find_by(username=user_info['username'])
    return u
