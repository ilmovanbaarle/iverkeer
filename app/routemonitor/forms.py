from django import forms
from django.forms import inlineformset_factory

from routemonitor.models import Project, Route


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'iv_project', 'description')


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('name', 'points', 'description', 'routeType')


RouteInlineFormset = inlineformset_factory(
    Project,
    Route,
    form=RouteForm,
    extra=1,
    max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)