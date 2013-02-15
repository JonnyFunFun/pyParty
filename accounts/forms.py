from django import forms
from models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab


class ProfileForm(forms.ModelForm):
    # Extra items
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', 'hostname', 'flags', )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = '/accounts/profile/save/'
    helper.form_enctype = 'multipart/form-data'
    helper.layout = Layout(
        TabHolder(
            Tab('Profile',
                Field('username', css_class='input-xlarge'),
                Field('first_name', css_class='input-xlarge'),
                Field('last_name', css_class='input-xlarge'),
                Field('quote', css_class='input-xlarge'),
                Field('avatar')
            ),
            Tab('About Me',
                Field('about_me')
            ),
            Tab('Rig Information',
                Div(
                    Field('processor'),
                    Field('processor_family'),
                    Field('processor_speed'),
                    css_class='well',
                ),
                Div(
                    Field('graphics'),
                    Field('graphics_model'),
                    Field('graphics_memory'),
                    css_class='well',
                ),
                Div(
                    AppendedText('memory', 'gb'),
                    Field('memory_type'),
                    css_class='well',
                ),
                Div(
                    AppendedText('hdd_space', 'gb'),
                    css_class='well',
                ),
                Div(
                    Field('case'),
                    Field('monitor'),
                    css_class='well',
                )
            )
        ),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
            )
    )