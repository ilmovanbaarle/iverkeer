from datetime import datetime
import logging
from unicodedata import name

from django.conf import settings
import requests
import urllib.parse as urlparse
from django.utils import timezone
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc

from routemonitor.models import Project, RouteData

logger = logging.getLogger(__name__)

def route_update():
    """ Updates all enabled (time is after start time, and before end time) routes travel information """
    #routes = Route.objects.filter(enabled=True).values('name', 'routepoints')
    thistime = timezone.now()
    thistime = thistime.strftime('%Y-%m-%d %H:%M%z')
    logger.warning(f'Dit is de tijd: {thistime}')

    routes = Project.objects.filter(start_date__lte = thistime)
    routes = routes.filter(end_date__gte = thistime).values('name', 'routepoints','routeType','traffic','travelMode','avoid')
    logger.warning(f'Dit komt uit het filter: {routes}')

    logger.info('Starting updating routes')
    if not routes:
        logger.info('No routes available for updating; skipping...')
        return
    for name in routes:
        #logger.warning(f'Dit is de description: {name["description"]}')
        key = "QGd3QJ7EOabPy30MKcNTBVahgVGtLqQk"
        #start = "51.89236,4.55976"
        #end = "51.94200,4.48367"
        routepoints = name["routepoints"]
        routeType = name["routeType"]             # Fastest route
        traffic = str(name["traffic"]).lower()    # To include Traffic information
        travelMode = name["travelMode"]           # Travel by truck
        avoid = name["avoid"]                     # Avoid unpaved roads
        #departureTime = "2022-01-25T14:28:00"
        departureTime = datetime.now().strftime('%Y-%m-%dT%H:%M:00')

        # Building the request URL
        baseUrl = "https://api.tomtom.com/routing/1/calculateRoute/";

        requestParams = (
            urlparse.quote(routepoints).replace(" ", "")
            #routepoints
            #urlparse.quote(start) + ":" + urlparse.quote(end) 
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
                project = Project.objects.get(name=name["name"]),
                travel_time = travelTime,
                delay = trafficDelay,
                route_length = lengthInMeters
            )
            logger.info(f'Route data toegevoegd voor route: {name["name"]}')

        else:
            logger.warning(f'Tomtom returned an error! Response: {response.status_code}')
    logger.info('Updated all route information')