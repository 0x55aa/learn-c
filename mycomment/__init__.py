from mycomment.models import Comment
from mycomment.forms import CommentForm


def get_model():
    return Comment


def get_form():
    return CommentForm
