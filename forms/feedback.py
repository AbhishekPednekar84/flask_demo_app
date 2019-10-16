from flask_wtf import FlaskForm
from wtforms import RadioField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import Length


class FeedbackForm(FlaskForm):
    feedback_score = RadioField("Options",
                                coerce=int,
                                choices=[(1, "One"),
                                         (2, "Two"),
                                         (3, "Three"),
                                         (4, "Four"),
                                         (5, "Five")], default=5)
    question1 = BooleanField("Our farm fresh organic produce")
    question2 = BooleanField("Packaging")
    question3 = BooleanField("Delivery")
    question4 = BooleanField("Ease of payment")
    feedback = TextAreaField("Feedback", validators=[Length(max=1000)])
    submit = SubmitField("Submit Feedback")
