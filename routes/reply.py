from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
)

from models.message import Message
from models.reply import Reply
from models.user import User
from routes import current_user

main = Blueprint('reply', __name__)


def users_from_content(content):
    parts = content.split(" ")
    users = []
    for p in parts:
        if p.startswith("@"):
            username = p[1:]
            u = User.find_by(username=username)
            if u is not None:
                users.append(u)
    return users


def send_email(sender, receiver, content):
    for r in receiver:
        form = dict(
            title='你被{} AT了'.format(sender.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id,
        )
        Message.new(form)


@main.route('/add', methods=["POST"])
def add():
    form = request.form
    u = current_user()
    content = form.get('content')
    users = users_from_content(content)
    if len(users) > 0:
        send_email(u, users, content)
    r = Reply.new(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=r.topic_id))
