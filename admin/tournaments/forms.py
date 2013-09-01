from django import forms
from tourneys.models import Tournament
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab


class SimpleTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament

    helper = FormHelper()
    helper.form_enctype = 'multipart/form-data'
    helper.form_action = '/admin/tournaments/save/'
    helper.layout = Layout(
        Field('name'),
        Field('game'),
        Field('starts'),
        Field('ends'),
        Field('team_size'),
        FormActions(
            Submit('add', 'Create Tournament', css_class="btn-primary")
        )
    )