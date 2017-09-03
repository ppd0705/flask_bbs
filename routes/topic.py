import time
from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from routes import (
    csrf_tokens,
    current_user,
    new_csrf_token
)

main = Blueprint('topic', __name__)


@main.route('/<int:id>', methods=["GET"])
def detail(id):
    m = Topic.get(id)
    token = new_csrf_token()
    return render_template('topic/detail.html', topic=m, token=token)


@main.route('/delete')
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    if u.id == 1 or u.id == Topic.find(id).user_id:
        # 管理员或话题创建者才有权限
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            # 验证token
            Topic.delete(id)
            Reply.delete_all(dict(topic_id=id))
    csrf_tokens.pop(token)
    return redirect(url_for('index.index'))


@main.route('/new', methods=["GET"])
def new():
    board_id = int(request.args.get('board_id', -1))
    token = new_csrf_token()
    bs = Board.all()
    return render_template('topic/new.html', bs=bs, token=token, bid=board_id)


@main.route('/add', methods=["POST"])
def add():
    form = request.form
    u = current_user()
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        t = Topic.new(form, user_id=u.id)
        csrf_tokens.pop(token)
        return redirect(url_for('topic.detail', id=t.id))
    else:
        abort(403)


@main.route('/edit', methods=["GET"])
def edit():
    id = int(request.args.get('id'))
    topic = Topic.find(id)
    board_id = int(request.args.get('board_id', -1))
    token = new_csrf_token()
    bs = Board.all()
    return render_template('topic/edit.html', topic=topic, bs=bs, token=token, bid=board_id)


@main.route('/update', methods=["POST"])
def update():
    u = current_user()
    form = request.form.to_dict()
    id = int(form.pop('id'))
    form['board_id'] = int(form.get('board_id'))
    form['updated_time'] = int(time.time())
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        Topic.update(id, form)
        csrf_tokens.pop(token)
        return redirect(url_for('topic.detail', id=id))
    else:
        abort(403)
