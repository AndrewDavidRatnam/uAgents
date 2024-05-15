"""
create a cleaning_proto object using the agents Protocol class. 
We give it the name cleaning and the version 0.1.0. T
his protocol will be used to define handlers and manage communication between agents
 using the defined message models
 """
from datetime import datetime, timedelta
from typing import List

"""
Geopy is a Python library that provides geocoding (converting addresses to geographic coordinates) 
and reverse geocoding (converting geographic coordinates to addresses) functionalities. 
It abstracts the complexities of various geocoding APIs and services, 
allowing developers to perform these tasks easily within their Python applications.
"""
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from uagents import Context, Model, Protocol
from .models import Provider, Availability, User

PROTOCOL_NAME = "cleaning"
PROTOCOL_VERSION = "0.1.0"

class ServiceRequest(Model):
    user: str
    location: str
    time_start: datetime
    duration: timedelta
    services: List[int]
    max_price: float

class ServiceResponse(Model):
    accept: bool
    price: float

class ServiceBooking(Model):
    location: str
    time_start: datetime
    duration: timedelta
    services: List[int]
    price: float

class BookingResponse(Model):
    success: bool

cleaning_proto = Protocol(name=PROTOCOL_NAME, version=PROTOCOL_VERSION)

def in_service_region(
        location: str, availability: Availability, provider: Provider
) -> bool :
    geolocator = Nominatim(user_agent="micro_agents")

    user_location = geolocator.geocode(location)
    cleaner_location = geolocator.geocode(provider.location)

    if user_location is None:
        raise RuntimeError(f"user location {location} not found")
    
    if cleaner_location is None:
        raise RuntimeError(f"provider location {provider.location} not found")
    
    cleaner_coordinates = (cleaner_location.latitude, cleaner_location.longitude)
    user_coordinates = (user_location.latitude, user_location.longitude)

    service_distance = geodesic(user_coordinates, cleaner_coordinates).miles
    in_range = service_distance <= availability.max_distance

    return in_range

@cleaning_proto.on_message(model=ServiceRequest, replies=ServiceResponse)
async def handle_query_request(ctx: Context, sender: str, msg: ServiceRequest):
    pass



