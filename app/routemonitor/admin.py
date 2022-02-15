#from django.contrib import admin
from django.contrib.gis import admin
from routemonitor.models import Project, RouteData, Route, Schedule

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

admin.site.register(Schedule)
admin.site.register(RouteData)
