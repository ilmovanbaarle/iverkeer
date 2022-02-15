from email.policy import default
import uuid

#from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Project(models.Model):
    name = models.CharField(max_length=50, unique= True, help_text='Gebruik een duidelijke naam. Bijvoorbeeld: Regelscenario wedstrijd Ajax')
    iv_project = models.CharField(max_length=50, help_text='Gebruik de Iv projectcode, bijvoorbeeld INFR191089.')
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(
        User,
        related_name="collections", 
        blank=True, null=True,
        on_delete=models.SET_NULL
        )
    description = models.TextField(blank = True, help_text='Eventuele aanvullende opmerkingen')

    def __str__(self):     
         return self.name 

class Route(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="route", on_delete=models.CASCADE
        )
    name = models.CharField(max_length=50, unique= True, help_text='Gebruik een duidelijke naam. Bijvoorbeeld: Omleidingsroute via A58-A2 2022-W12')
    points =  models.MultiPointField()
    description = models.TextField(blank = True, help_text='Eventuele aanvullende opmerkingen')

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
    traffic = models.BooleanField(default=True, help_text="Determines whether current traffic is used in route calculations")
    avoid = models.CharField(max_length=50, default="unpavedRoads", editable=False)

    def __str__(self):     
         return self.name 

class Schedule(models.Model):
    route = models.ForeignKey(
        Route,
        related_name="schedule", on_delete=models.CASCADE
        )
    name = models.CharField(max_length=50, unique= False, help_text='Gebruik een duidelijke naam. Bijvoorbeeld: Zaterdag overdag')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):     
         return self.name 

class RouteData(models.Model):
    route = models.ForeignKey(
        Route,
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
        verbose_name = 'Route data'
        verbose_name_plural = 'Route data'
        get_latest_by = 'timestamp'

    def __str__(self):
        return f'[{self.route}] om {self.timestamp}'