from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from admin.settings import get_setting


class SettingsForm(forms.Form):
    site_name = forms.CharField(initial=get_setting('site_name'))

    site_title = forms.CharField(
        initial=get_setting('site_title'),
        help_text="Top-left header text, HTML allowed"
    )

    welcome_msg = forms.CharField(
        widget=forms.Textarea,
        label="Welcome message",
        initial=get_setting('welcome_msg'),
        help_text="Message displayed on the header on a users' dashboard"
    )

    lan_name = forms.CharField(initial=get_setting('lan_name'))

    goodbye_survey = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Goodbye Survey",
        initial=(get_setting('goodbye_survey') == '1')
    )

    enable_music = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Music",
        initial=(get_setting('enable_music') == '1')
    )

    enable_servers = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Servers",
        initial=(get_setting('enable_servers') == '1')
    )

    enable_tournaments = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Tournaments",
        initial=(get_setting('enable_tournaments') == '1')
    )

    enable_noms = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Nom-nom-noms",
        initial=(get_setting('enable_noms') == '1')
    )

    enable_benchmarks = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Benchmarks",
        initial=(get_setting('enable_benchmarks') == '1')
    )

    enable_gallery = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Gallery",
        initial=(get_setting('enable_gallery') == '1')
    )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = '/admin/settings/save/'
    helper.layout = Layout(
        TabHolder(
            Tab('System Settings',
                Field('site_name', css_class='input-xlarge'),
                Field('site_title', rows="3", css_class='input-xlarge'),
                Field('welcome_msg', rows="3", css_class='input-xlarge'),
                Field('lan_name', css_class='input-xlarge'),
                Field('goodbye_survey')
            ),
            Tab('Enabled Modules',
                Field('enable_music'),
                Field('enable_servers'),
                Field('enable_tournaments'),
                Field('enable_noms'),
                Field('enable_benchmarks'),
                Field('enable_gallery'),
            )
        ),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )