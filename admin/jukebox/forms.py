from django import forms
from music.models import MusicSource
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions


class NewMusicSourceForm(forms.ModelForm):
    class Meta:
        model = MusicSource

    helper = FormHelper()
    helper.form_enctype = 'multipart/form-data'
    helper.form_action = '/admin/music/source/add'
    helper.layout = Layout(
        Field('path'),
        FormActions(
            Submit('add', 'Add source', css_class="btn-primary"),
        )
    )