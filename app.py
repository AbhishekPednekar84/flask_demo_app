import flask
from db import db
from lm import login_manager
from config import Config

# This tells login_required what out user view is
login_manager.login_view = "user.login"

# This changes the flashed message for login_required
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = flask.Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from views import feedback_views
    from views import login_views
    from views import register_views
    from views import home_views

    app.register_blueprint(feedback_views.feedback_blueprint)
    app.register_blueprint(login_views.blueprint)
    app.register_blueprint(register_views.blueprint)
    app.register_blueprint(home_views.home_blueprint)

    return app


if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    app.run()
