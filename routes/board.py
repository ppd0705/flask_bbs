from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
)
from models.board import Board
from routes import (
    current_user,
    csrf_tokens,
    new_csrf_token,
)

main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    token = new_csrf_token()
    bs = Board.all()
    return render_template('board/admin_index.html', token=token, bs=bs)


@main.route('/add', methods=["POST"])
def add():
    form = request.form
    token = request.args.get('token')
    u = current_user()
    if u.id == 1 and token in csrf_tokens and csrf_tokens[token] == u.id:
        # 验证token和id
        Board.new(form)
        csrf_tokens.pop(token)
    return redirect(url_for('.index'))
