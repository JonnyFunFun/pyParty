from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab
from settings import get_setting

class SettingsForm(forms.Form):
    site_name = forms.CharField()

    enable_music = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Music",
        initial=get_setting('enable_music')
    )

    enable_servers = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Servers",
        initial=get_setting('enable_servers')
    )

    enable_tournaments = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Tournaments",
        initial=get_setting('enable_tournaments')
    )

    enable_noms = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Nom-nom-noms",
        initial=get_setting('enable_noms')
    )

    enable_benchmarks = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Benchmarks",
        initial=get_setting('enable_benchmarks')
    )

    enable_gallery = forms.ChoiceField(
        widget=forms.CheckboxInput,
        label="Gallery",
        initial=get_setting('enable_gallery')
    )

    radio_buttons = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', "Option two can is something else and selecting it will deselect option one")
            ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )

    enabled_modules = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
            ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )

    appended_text = forms.CharField(
        help_text = "Here's more help text"
    )

    prepended_text = forms.CharField()

    prepended_text_two = forms.CharField()

    multicolon_select = forms.MultipleChoiceField(
        choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = '/admin/settings/save/'
    helper.layout = Layout(
        TabHolder(
            Tab('System Settings',

                Field('site_name', css_class='input-xlarge'),
                Field('textarea', rows="3", css_class='input-xlarge'),
                'radio_buttons',
                Field('enabled_modules', style="background: #FAFAFA; padding: 10px;"),
                AppendedText('appended_text', '.00'),
                PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
                PrependedText('prepended_text_two', '@'),
                'multicolon_select',
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