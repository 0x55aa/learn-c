# coding:utf-8
from django import forms
from django.contrib.comments.forms import CommentSecurityForm
from mycomment.models import Comment


class CommentForm(CommentSecurityForm):
    comment = forms.CharField(label='评论', widget=forms.Textarea, max_length=300)

    def get_comment_model(self):
        return Comment

    def get_comment_create_data(self):
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_text(self.target_object._get_pk_val()),
            user_name    = self.cleaned_data["comment"],
            submit_date  = timezone.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,

        )
