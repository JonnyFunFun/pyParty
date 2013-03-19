from django import forms
from servers.models import Server
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab


class GameServerForm(forms.ModelForm):
    class Meta:
        model = Server

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_enctype = 'multipart/form-data'
    helper.form_action = '/admin/servers/save/'
    helper.layout = Layout(
        TabHolder(
            Tab('Basic Info',
                Field('name'),
                Field('game'),
                Field('server_type'),
                Field('operator'),
                Field('address'),
                Field('port'),
                Field('mod_approved')
            ),
            Tab('Server Description',
                Field('desc')
            )
        ),

        FormActions(
            Submit('add', 'Save server', css_class="btn-primary"),
            Submit('cancel', 'Cancel')
        )
    )