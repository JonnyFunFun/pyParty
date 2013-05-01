from django import forms
from models import SurveyEntry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab


class DepartingSurvey(forms.ModelForm):
    class Meta:
        model = SurveyEntry
        exclude = ('User',)

    helper = FormHelper()
    helper.form_action = '/accounts/goodbye/finish/'
    helper.form_enctype = 'multipart/form-data'
    helper.layout = Layout(
        Field('lan_rating', css_class='input-xlarge'),
        Field('pyp_rating', css_class='input-xlarge'),
        Field('complaints', css_class='input-xlarge'),
        Field('improvements', css_class='input-xlarge'),
        Field('returning', css_class='input-xlarge'),
        FormActions(
            Submit('save_changes', 'Submit Survey and Depart', css_class="btn-primary")
        )
    )