import click
from flask.cli import with_appcontext
from db import db
from models.models import UserModel, FeedbackModel


@click.command(name="create_tables")
@with_appcontext
def create_tables():  # pragma: no cover
    db.create_all()
