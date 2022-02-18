from django.shortcuts import render

# Create your views here.

from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse

from routemonitor.models import Project
from routemonitor.forms import ProjectForm, RouteInlineFormset


class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template_name = 'project/project_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)

        context['route_formset'] = RouteInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        route_formset = RouteInlineFormset(self.request.POST)
        if form.is_valid() and route_formset.is_valid():
            return self.form_valid(form, route_formset)
        else:
            return self.form_invalid(form, route_formset)

    def form_valid(self, form, route_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving Route Instances
        routes = route_formset.save(commit=False)
        for route in routes:
            route.project = self.object
            route.save()
        #return redirect(reverse("project:project_create"))

    def form_invalid(self, form, route_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  route_formset=route_formset
                                  )
        )