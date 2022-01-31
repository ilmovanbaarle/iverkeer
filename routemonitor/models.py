from email.policy import default
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator

class Project(models.Model):
    name = models.CharField(max_length=50, unique= True, help_text='Use a clear and distinctive name for the route.')
    project = models.CharField(max_length=50, help_text='Use the Iv project code, for example INFR191089.')
    routepoints = models.CharField(max_length=200, help_text='For now use Google Maps coordinates. "51.89236,4.55976:51.94200,4.48367".')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    description = models.TextField(blank = True)

    #Dit zijn route-opties van Tomtom
    ROUTE_CHOICES = (
        ('fastest','fastest'),
        ('shortest', 'shortest'),
        ('eco','eco'),
        ('thrilling','thrilling'),
    )
    routeType = models.CharField(max_length=10, choices=ROUTE_CHOICES, default ='fastest', help_text="Leave this at 'fastest' unless you know what you are doing.")

    TRAVEL_MODE_CHOICES = (
        ('car','car'),
        ('truck', 'truck'),
        ('taxi','taxi'),
        ('bus','bus'),
        ('motorcycle', 'motorcycle'),
        ('bicycle', 'bicycle'),
        ('pedestrian', 'pedestrian')
    )
    travelMode = models.CharField(max_length=20, choices=TRAVEL_MODE_CHOICES, default ='car', help_text="The mode of travel for the requested route.")
    traffic = models.BooleanField(default=True, help_text="Determines whether current traffic is used in route calculations.")
    avoid = models.CharField(max_length=50, default="unpavedRoads", editable=False)

    def __str__(self):     
         return self.name 

class RouteData(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='data',
    )
    timestamp = models.DateTimeField(default=timezone.now)
    
    travel_time = models.DecimalField(
        decimal_places=2,
        max_digits=9,
    )   
    route_length = models.DecimalField(
        decimal_places=2,
        max_digits=9,
    )
    delay = models.DecimalField(
        decimal_places=2,
        max_digits=9,
    )  
    class Meta:
        verbose_name = 'Route historical data'
        verbose_name_plural = 'Route historical data'
        get_latest_by = 'timestamp'

    def __str__(self):
        return f'[{self.project}] at {self.timestamp}'