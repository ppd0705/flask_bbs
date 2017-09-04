import os
import uuid

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from models.user import User
from routes import current_user, csrf_tokens, new_csrf_token

main = Blueprint('user', __name__)


@main.route('/profile', methods=['GET'])
def profile():
    u = current_user()
    if u is None:
        return (redirect(url_for('index.index')))
    else:
        token = new_csrf_token()
        return render_template('user/profile.html', user=u, token=token)


@main.route('/setting', methods=['GET'])
def setting():
    u = current_user()
    if u is None:
        flash('请先登录')
        return (redirect(url_for('index.index')))
    else:
        token = new_csrf_token()
        return render_template('user/setting.html', user=u, token=token)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg', 'gif']
    return suffix in valid_type


@main.route('/image', methods=["POST"])
def change_avatar():
    u = current_user()
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        old_image = u.user_image
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('avatar', filename))
        u.user_image = '/user/avatar/' + filename
        u.save()
        # 若旧图片不为default.png，删除
        if 'default.png' not in old_image:
            os.remove(old_image.split('/', 2)[-1])
    return redirect(url_for('.setting'))


@main.route('/name', methods=["POST"])
def change_name():
    form = request.form
    name = form.get('name')
    signature = form.get('signature')
    u = current_user()
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u.validate_change_name(name, signature):
            flash('change name succeed ')
            return redirect(url_for('.setting'))
    flash('change name failed ')
    return redirect(url_for('.setting'))


@main.route('/pwd', methods=["POST"])
def change_pwd():
    form = request.form
    old_pwd = form.get('old_pass')
    new_pwd = form.get('new_pass')
    u = current_user()
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u.validate_change_pwd(old_pwd, new_pwd):
            flash('change pwd succeed')
            return redirect(url_for('.setting'))
    flash('change pwd failed')
    return redirect(url_for('.setting'))


@main.route('/<int:id>', methods=['GET'])
def user_detail(id):
    u = User.find(id)
    if u is None:
        abort(404)
    else:
        token = new_csrf_token()
        return render_template('user/user_detail.html', user=u, token=token)


@main.route('/avatar/<filename>', methods=["GET"])
def uploads(filename):
    return send_from_directory('avatar', filename)
