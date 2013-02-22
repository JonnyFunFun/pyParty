from django import forms
from accounts.models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab


FLAG_CHOICES = (
    ('on', True),
    (True, True),
    ('off', False),
    (False, False),
)


class AdminProfileForm(forms.ModelForm):
    # Extra items
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    admin = forms.ChoiceField(
        widget=forms.CheckboxInput,
        choices=FLAG_CHOICES
    )
    op = forms.ChoiceField(
        widget=forms.CheckboxInput,
        choices=FLAG_CHOICES
    )
    vip = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="VIP",
        choices=FLAG_CHOICES
    )

    class Meta:
        model = UserProfile
        exclude = ('user', 'flags', )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_enctype = 'multipart/form-data'
    helper.layout = Layout(
        TabHolder(
            Tab('Profile',
                Field('username', css_class='input-xlarge'),
                Field('first_name', css_class='input-xlarge'),
                Field('last_name', css_class='input-xlarge'),
                Field('quote', css_class='input-xlarge'),
                Field('avatar'),
                Field('hostname', css_class='input-xlarge'),
            ),
            Tab('About Them',
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
            ),
            Tab('Permissions & Flags',
                Field('admin'),
                Field('op'),
                Field('vip'),
            )
        ),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
            )
    )