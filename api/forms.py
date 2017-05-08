from django import forms


class StepsForm(forms.Form):
    """Validates API requests to /api/steps/<step_type>"""
    lesson = forms.IntegerField(required=True, min_value=0)
