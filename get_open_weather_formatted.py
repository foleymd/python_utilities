''' getting weather from openweathermap.org based on command line args and
    prints formatted data
    example on command line:
    python3 get_open_weather_formatted.py 30.266666 -97.733330 minutely,hourly,daily
    API docs: https://openweathermap.org/api
'''

import json
import requests
import sys
import pprint
import pytz
from datetime import datetime
from geopy import Nominatim
from timezonefinder import TimezoneFinder
from secret import open_weather_appid


def command_line_input():
    # exit if you don't get three arguments in variable assignment
    if len(sys.argv) < 3:
        print('Command should be: python3 get_open_weather.py lat lon exclude')
        sys.exit()

    # latitude and longitude + which types of data to exclude:a
    # current,minutely hourly daily alerts
    arg1, arg2, arg3 = str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])

    return arg1, arg2, arg3


# converts meteorological degrees to a cardinal direction
def degrees_to_cardinal(degrees):

    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((degrees + 11.25)/22.5 - 0.02)

    return directions[ix % 16]

# final print


def display_weather(weather):

    display_width = 0

    # determining width of longest item
    for item in weather:
        if len(item) > display_width:
            display_width = len(item)

    # setting display width based on above length for pretty output
    string_width = display_width + 4
    separator_width = string_width + 2
    vertical_separator = '-' * separator_width

    # printing each item separated by a line for clarity
    for item in weather:
        print(vertical_separator)
        print('|' + str(item).center(string_width, ' ') + '|')

    # displaying final line to complete the box
    print(vertical_separator)


# standardized temperature output
def format_temp(temp):

    temp = str(round(temp, 1)) + u"\N{DEGREE SIGN}" + 'F'
    return temp


# formats current weather data
def format_weather_data(weather, location, tz):

    header = 'Current Weather'

    # converting to month/day/year & 12-hr time based on time zone
    date = str(datetime.fromtimestamp(
        weather["dt"], tz).strftime('%m/%d/%Y %I:%M %p'))

    description = weather["weather"][0]["description"].title()

    # rounds and adds degree symbol + Fahrenheit
    temp = format_temp(weather["temp"])
    feels_like = format_temp(weather["feels_like"])
    temps = str('Temp: ' + temp + '    ' + 'Feels Like: ' + feels_like)

    # sunrise and sunset human-readable time based on time zone
    sunrise = datetime.fromtimestamp(
        weather["sunrise"], tz).strftime('%I:%M %p')
    sunset = datetime.fromtimestamp(weather["sunset"], tz).strftime('%I:%M %p')
    sun = str('Sunrise: ' + sunrise + '     ' + 'Sunset: ' + sunset)

    # adding units + direction of wind
    wind_speed = str(round(weather["wind_speed"], 1)) + ' mph'
    wind_deg = str(degrees_to_cardinal(weather["wind_deg"]))
    wind = str('Winds: ' + wind_deg + ' ' + wind_speed)

    # more formatting
    pressure = 'Pressure: ' + str(weather["pressure"]) + ' hPa (millibars)'
    humidity = 'Humidity: ' + str(weather["humidity"]) + '%'
    dew_point = 'Dew point: ' + format_temp(weather["dew_point"])

    # convert feet to miles, round
    visibility = 'Visibility: ' + \
        str(round(weather["visibility"] / 1609.34, 1)) + ' miles'

    # returned in order desired for display
    formatted_weather = [header,
                         location,
                         date,
                         description,
                         temps,
                         sun,
                         wind,
                         pressure,
                         humidity,
                         dew_point,
                         visibility,
                         ]

    return formatted_weather


# performs request.get for weather data and returns a dict with formatted data
def get_weather(lat, lon, exclude):

    # creating url with sys.args added to query+ specifying imperial units
    url = 'https://api.openweathermap.org/data/2.5/onecall?units=imperial&lat=%s&lon=%s&exclude=%s&appid=%s' % (
        lat, lon, exclude, open_weather_appid)

    # requesting data for url and raising error if necessary
    response = requests.get(url)
    response.raise_for_status()

    # formats json into python data structures
    current_weather_data = json.loads(response.text)["current"]

    return current_weather_data


def get_location_data(lat, lon):

    # Nominatim takes combined lat and lon in one argument
    input_location = str(lat + ', ' + lon)

    # user_agent can be any email address
    geolocator = Nominatim(user_agent="email@gmail.com")

    # actual call to get location data
    location = geolocator.reverse(input_location)

    # the location includes a ton of data - getting the raw data to provide
    # more generic information
    address = location.raw['address']
    display_location = ", ".join(
        [address.get('city', ''), address.get('state', ''), address.get('country', '')])

    # timezone processing requires lat and lon to be separate floats, though
    latitude, longitude = float(lat), float(lon)
    tz = pytz.timezone(TimezoneFinder().timezone_at(
        lng=longitude, lat=latitude))

    return display_location, tz


def main():

    # user-input data from command line
    lat, lon, exclude = command_line_input()

    # api call returning raw data in a dictionary
    current_weather_data = get_weather(lat, lon, exclude)

    # using lat and lon to get readable location and timezone
    display_location, tz = get_location_data(lat, lon)

    # formatiing and displaying data returned by api
    try:
        formatted_current = format_weather_data(
            current_weather_data, display_location, tz)
        display_weather(formatted_current)
    except:
        print('Internal error: Skipping current weather.')
        pass


main()
