import flask
import app
from forms.feedback import FeedbackForm
from flask_login import login_required, current_user
from models.models import FeedbackModel
from models.models import UserModel

feedback_blueprint = flask.Blueprint("feedback", __name__, template_folder="templates")


@feedback_blueprint.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if current_user.feedback == "Y":
        return flask.render_template("feedback/disallow_feedback.html")

    form = FeedbackForm()
    if form.validate_on_submit():
        user_feedback = FeedbackModel(rating=form.feedback_score.data,
                                      question1=form.question1.data,
                                      question2=form.question2.data,
                                      question3=form.question3.data,
                                      question4=form.question4.data,
                                      comments=form.feedback.data,
                                      user_id=current_user.id)

        app.db.session.add(user_feedback)

        user = UserModel.query.filter_by(id=current_user.id).first()
        user.feedback = "Y"

        app.db.session.commit()
        return flask.render_template("feedback/feedback_success.html")

    return flask.render_template("feedback/feedback.html", form=form)


@feedback_blueprint.route("/success")
@login_required
def success():
    return flask.render_template("feedback/success_base.html")
