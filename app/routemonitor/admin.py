#from django.contrib import admin
from django.contrib.gis import admin
from routemonitor.models import Project, RouteData, Route, Schedule

from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'iv_project', 'created_date')
    list_filter = ('iv_project', 'name')
    search_fields = ['name']

@admin.register(Route)
class RouteAdmin(admin.OSMGeoAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'project', 'points', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('travelMode', 'routeType', 'traffic',),
        }),
    )

class RouteDataResource(resources.ModelResource):
    route__project__iv_project = Field(attribute='route__project__iv_project', column_name='IV-project')
    route__project__name = Field(attribute='route__project__name', column_name='Project')
    route__name = Field(attribute='route__name', column_name='Route')
    timestamp = Field(attribute='timestamp', column_name='Tijdstip', widget=DateTimeWidget(format="%Y-%m-%d %H:%M"))
    class Meta:
        model = RouteData
        fields = ('route__project__iv_project', 'route__project__name', 'timestamp', 'route__name', 'travel_time', 'delay', 'route_length')

admin.site.register(Schedule)
@admin.register(RouteData)
class RouteDataAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('route', 'travel_time', 'delay', 'timestamp')
    list_filter = ('route', 'timestamp')
    resource_class = RouteDataResource