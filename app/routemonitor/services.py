from datetime import datetime
import logging
from unicodedata import name

from django.conf import settings
import time
import requests
import urllib.parse as urlparse
from django.utils import timezone
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc
from django.contrib.gis.db.models.functions import AsGeoJSON

from routemonitor.models import Route, Schedule
from routemonitor.models import Project, RouteData


logger = logging.getLogger(__name__)

def route_update():
    thistime = timezone.now()
    thistime = thistime.strftime('%Y-%m-%d %H:%M%z')
    #logger.warning(f'Dit is de tijd: {thistime}')

    # Query eerst alle routes
    routes = Route.objects.all()
    routes = Route.objects.filter(
        schedule__start_date__lte = thistime,
        schedule__end_date__gte = thistime,
    )
    #logger.warning(f'Actieve routes: {routes}')

    routes = routes.values('name','points','routeType','traffic','travelMode','avoid')
    count = 0

    for route in routes:
        key = "QGd3QJ7EOabPy30MKcNTBVahgVGtLqQk"
        # Converteer de multipoints naar string en clean ze voor TomTom
        coordinates = ''
        count += 1
        if count % 5 == 0:
            time.sleep(1)
        for point in route["points"]:
            tuple = point.coords[::-1]
            tuple = str(tuple)
            logger.warning(tuple)
            tuple = tuple.replace(" ", "").replace("(", "").replace(")", "")
            coordinates = coordinates + tuple + ':'
        # Coordinaten staan verkeerdom opgeslagen voor TomTom
        coordinates = coordinates[:-1]
        # Haal de overige variabelen op
        routeType = route["routeType"]             # Fastest route
        traffic = str(route["traffic"]).lower()    # To include Traffic information
        travelMode = route["travelMode"]           # Travel by truck
        avoid = route["avoid"]                     # Avoid unpaved roads
        departureTime = datetime.now().strftime('%Y-%m-%dT%H:%M:00')    

        # Building the request URL
        baseUrl = "https://api.tomtom.com/routing/1/calculateRoute/";

        requestParams = (
            urlparse.quote(coordinates)
            + "/json?routeType=" + routeType
            + "&traffic=" + traffic
            + "&travelMode=" + travelMode
            + "&avoid=" + avoid 
            + "&departAt=" + urlparse.quote(departureTime)
        )

        requestUrl = baseUrl + requestParams + "&key=" + key

        # Sending the request
        response = requests.get(requestUrl)

        if(response.status_code == 200):
            # Get response's JSON
            jsonResult = response.json()

            # Read summary of the first route
            routeSummary = jsonResult['routes'][0]['summary'];
            travelTime = routeSummary['travelTimeInSeconds'] / 60
            lengthInMeters = routeSummary['lengthInMeters'] / 1000
            trafficDelay = routeSummary['trafficDelayInSeconds'] / 60

            RouteData.objects.create(
                route = Route.objects.get(name=route["name"]),
                travel_time = travelTime,
                delay = trafficDelay,
                route_length = lengthInMeters
            )
            logger.info(f'Route data toegevoegd voor route: {route["name"]}')
        else:
            logger.warning(f'ERROR: {response.status_code}')
