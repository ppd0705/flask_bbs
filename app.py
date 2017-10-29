from flask import Flask

from config import secret_key
from routes.board import main as board_routes
from routes.index import main as index_routes
from routes.message import main as message_routes
from routes.reply import main as reply_routes
from routes.topic import main as topic_routes
from routes.user import main as user_routes


def configured_app():

    app = Flask(__name__)

    app.secret_key = secret_key

    app.route()

    app.register_blueprint(index_routes)
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(message_routes, url_prefix='/message')
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(user_routes, url_prefix='/user')
    return app


if __name__ == '__main__':

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=8000,
        threaded=True,
    )

    app = configured_app()
    app.run(**config)
