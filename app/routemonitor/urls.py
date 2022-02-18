from django.urls import path
from routemonitor.views import ProjectCreateView
app_name = 'routemonitor'
urlpatterns = [
    # ...
    #path('projects', ProjectListView.as_view(), name="project_list"),
    path('projects/create', ProjectCreateView.as_view(), name="project_form"),
    # ...
]