import requests, requests_cache
import ssl, copy, datetime
from geopy.distance import vincenty
from prettytable import PrettyTable
import ConfigParser

requests_cache.install_cache('foursquare_cache')

config = ConfigParser.RawConfigParser()
config.read('config.ini')
auth_token = config.get('auth', 'auth_token')
foursquare_url = "https://api.foursquare.com/v2/users/self/checkins?oauth_token=%s&v=20140806&limit=%s&offset=%s&sort=oldestfirst"
total_distance = 0
prev_coords = None
airport_count = 0
unique_airport_count = 0
limit = 250
all_items = []
airports = {}
trips = [{'legs': []}]
trip_number = 0
trip_start = ''
home_airport = 'AUS'

#TODO: first call for total, determine if next page exists
for offset in (0, 250, 500):
  response = requests.get(foursquare_url % (auth_token, limit, offset))
  if response.status_code == 200:
    items = response.json()['response']['checkins']['items']
    all_items += items

if len(all_items) > 0:
  print "Total checkins: %s" % len(all_items)
  for item in all_items:
    venue = item['venue']
    venue_name = venue['name']
    created_at = datetime.datetime.fromtimestamp(item['createdAt'])
    location = venue['location']
    if 'city' in location:
      city = location['city']

    for category in venue['categories']:
      if category['name'] == 'Airport' and '(' in venue_name and ')' in venue_name:
        airport_count += 1
        if venue_name in airports:
          airports[venue_name] = airports[venue_name] + 1
        else:
          airports[venue_name] = 1

        # Calculate trips, store legs
        current_trip = trips[trip_number]
        current_trip['legs'].append(city)
        if len(current_trip['legs']) == 1:
          current_trip['depart'] = created_at
        #print "Number of cities: %d" % len(current_trip)
        #print "More than two legs? %d, Home airport? %s " % (len(current_trip) > 2, home_airport in venue_name)
        if len(current_trip['legs']) > 2 and home_airport in venue_name:
          # End of trip
          #print "Trip: %s:" % trip_number
          #print current_trip
          current_trip['return'] = created_at
          trip_number += 1
          trips.append({'legs': [], 'depart': created_at})

        #Calculcate distance per leg
        coords = (location['lat'], location['lng'])
        if prev_coords:
          distance = vincenty(coords, prev_coords).miles
          total_distance += distance
          #print("%s: Distance from %s -> %s: %d" % (str(created_at), prev_venue_name, venue_name, distance))
        prev_coords = copy.copy(coords)
        prev_venue_name = copy.copy(venue_name)

  airport_table = PrettyTable(['Airport', 'Visits'])
  airport_table.sortby = 'Visits'
  airport_table.reversesort = True
  for airport in airports:
    airport_table.add_row([airport, airports[airport]])

  trip_table = PrettyTable(['Depart', 'Return', 'Legs'])
  for trip in trips:
    legs = ''
    for leg in trip['legs']:
      legs = legs + ', ' + leg
    return_date = ''
    if 'return' in trip:
      return_date = trip['return']
      return_string = "%s-%s-%s" % (str(return_date.year), str(return_date.month), str(return_date.day))
      depart_string = "%s-%s-%s" % (str(trip['depart'].year), str(trip['depart'].month), str(trip['depart'].day))
    trip_table.add_row([depart_string, return_string, legs])


  print "Airport checkins: %s" % airport_count
  print "Total trips: %d" % len(trips)
  print "Total flying distance: %d" % round(total_distance)
  print "Unique airports: %s" % len(airports)
  print "Trips: \n%s" % trip_table
  #print trips
  print "Airports: \n%s" % airport_table
else:
  print('Error calling API: '+response.text)
