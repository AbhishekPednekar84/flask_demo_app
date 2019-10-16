import flask
import app
from forms.register import RegisterForm
from models.models import UserModel
from flask_login import current_user

blueprint = flask.Blueprint("register", __name__, template_folder="templates")


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("feedback.feedback"))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = UserModel.hash_password(form.password.data)
        user = UserModel(name=form.name.data, email=form.email.data.lower(), password=hashed_password)

        if UserModel.verify_email(form.email.data):
            flask.flash("An account with this email already exists", "danger")
        else:
            try:
                app.db.session.add(user)
                app.db.session.commit()
                flask.flash(f"The account for {form.email.data} has been created", "success")
                return flask.redirect(flask.url_for("user.login"))
            except Exception as e: # pragma: no cover
                print(e)
    return flask.render_template("user/register.html", form=form)


