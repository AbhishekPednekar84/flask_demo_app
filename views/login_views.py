from flask import current_app, Blueprint, url_for, redirect, request, render_template, flash
from forms.login import LoginForm
from models.models import UserModel
from flask_login import login_user, current_user, logout_user
from app import db

blueprint = Blueprint("user", __name__, template_folder="templates")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("feedback.feedback"))
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data.lower()).first()
        if user and UserModel.verify_password(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("feedback.feedback"))
        else:
            flash(f"Please check your credentials", "danger")
    return render_template("user/login.html", form=form)


@blueprint.route("/logout")
def logout():
    # Before logging out, set the feedback flag in the UserModel model to N
    user = UserModel.query.filter_by(id=current_user.id).first()
    user.feedback = "N"
    db.session.commit()

    logout_user()

    return redirect(url_for("home.home"))
