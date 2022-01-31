from django.contrib import admin
from routemonitor.models import Project, RouteData


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'start_date', 'end_date')
    list_filter = ('project', 'start_date')
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': ('name', 'project','routepoints', 'start_date', 'end_date', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('travelMode', 'routeType', 'traffic',),
        }),
    )

@admin.register(RouteData)
class RouteHistoryAdmin(admin.ModelAdmin):
    list_display = ('project', 'timestamp', 'travel_time', 'delay')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)