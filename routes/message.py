from flask import (
    Blueprint,
    flash,
    request,
    redirect,
    url_for,
    render_template,
)
from models.message import Message
from routes import (
    csrf_tokens,
    current_user,
    new_csrf_token,
)

main = Blueprint('message', __name__)


@main.route('/add', methods=["POST"])
def add():
    form = request.form
    u = current_user()
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        Message.new(form, sender_id=u.id)
        csrf_tokens.pop(token)
    return redirect(url_for('.index'))


@main.route('/', methods=["GET"])
def index():
    u = current_user()
    if u is None:
        flash('请先登录')
        return redirect(url_for('index.index'))
    else:
        token = new_csrf_token()
        send_message = Message.find_all(sender_id=u.id)
        received_message = Message.find_all(receiver_id=u.id)
        t = render_template(
            "message/index.html",
            sends=send_message,
            receives=received_message,
            token=token
        )
        return t


@main.route("/view/<int:id>")
def view(id):
    message = Message.find(id)
    if current_user().id == message.receiver_id:
        message.mark_read()
    if current_user().id in [message.sender_id, message.receiver_id]:
        return render_template("message/detail.html", message=message)
    else:
        return redirect(url_for(".index"))
