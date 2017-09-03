from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from models.board import Board
from models.topic import Topic
from models.user import User
from routes import new_csrf_token, current_user

main = Blueprint('index', __name__)


@main.route('/', methods=["GET"])
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    return render_template('index.html', ms=ms, token=token, bs=bs, bid=board_id)


@main.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        token = new_csrf_token()
        return render_template('user/register.html', token=token)
    else:
        form = request.form
        if User.validate_register(form):
            flash('注册成功')
            return redirect(url_for('.login'))
        else:
            flash('注册失败')
            return redirect(url_for('.register'))


@main.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        token = new_csrf_token()
        return render_template('user/login.html', token=token)
    else:
        form = request.form
        u = User.validate_login(form)
        if u is not None:
            session['user_id'] = u.id
            return redirect(url_for('.index'))
        else:
            flash('用户名或密码有误')
            return redirect(url_for('.login'))


@main.route('/logout', methods=["GET"])
def logout():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        session.pop('user_id', None)
        return redirect(url_for('.login'))


@main.route('/about', methods=["GET"])
def about():
    token = new_csrf_token()
    return render_template('about.html', token=token)
