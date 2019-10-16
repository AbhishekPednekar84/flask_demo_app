import flask

home_blueprint = flask.Blueprint("home", __name__, template_folder="templates")


@home_blueprint.route("/")
def home():
    return flask.render_template("home/home.html")