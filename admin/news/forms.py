from announcements.models import Announcement
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement

    helper = FormHelper()
    helper.form_enctype = 'multipart/form-data'
    helper.form_action = '/admin/news/new/'
    helper.layout = Layout(
        Field('title'),
        Field('body'),

        FormActions(
            Submit('add', 'Post Announcement', css_class="btn-primary")
        )
    )