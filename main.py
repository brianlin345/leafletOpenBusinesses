from flask import Flask, current_app, render_template, request, jsonify, redirect, url_for

import requests
import json, csv
from datetime import datetime
from geojson import Feature, FeatureCollection, Point, dump
import time
from operator import add


class yelpQuery:
    yelp_url = "https://api.yelp.com/v3/businesses/search"
    api_key = "Ph5ToEVanaZhUmnCWJDAWFnlCah55sgnz3r91I-sC6ObZI8KCAyXDtI4cAqs7hoUg0GgquEJCnHhMBBoXfe6P2uPgafPpa5GkDLAGDtbeliu2JzileqOOHdPAN6zXXYx"
    business_keys = ['id', 'name', 'latitude', 'longitude', 'price', 'rating', 'url']
    max_searches = 3
    radius = 2000
    bucket_name = "leaflet-open-businesses-bucket"

    def __init__(self, lat, lon, time, filename='businesses'):
        """Sets location and API request parameters"""
        self.latitude = lat
        self.longitude = lon
        self.radius = yelpQuery.radius
        self.time = time
        self.filename = filename
        self.headers = {'Authorization': 'Bearer %s' % yelpQuery.api_key}
        self.business_dict = {business_key:[] for business_key in yelpQuery.business_keys}
        self.search_count = 0
        self.search_offset = 0

        #self.client = storage.Client()
        #self.bucket = client.get_bucket(yelpQuery.bucket_name)


    def yelp_main(self):
        """Controls full Yelp API request sequence"""
        self.yelp_search()
        self.batch_yelp_search()
        self.make_list()
        self.writeJSON_direct()

    def yelp_search(self):
        """Makes Yelp API Request with handling for request errors"""
        self.params = {'latitude': self.latitude, 'longitude': self.longitude, 'radius': self.radius, 'open_at': self.time, 'limit': 50, 'offset': self.search_offset}
        self.req = requests.get(yelpQuery.yelp_url, params = self.params, headers= self.headers)
        if self.req.status_code == 200:
            return self.req
        else:
            print('JSON status code:{}'.format(self.req.status_code))

    def parse_businesses(self):
        """Parses JSON from Yelp API - separates into needed variables and prepares variables for later API requests"""
        businesses_parsed = self.businesses['businesses']
        offset_change = 0

        for business in businesses_parsed:
            curr_distance = self.calc_distance(business['coordinates']['latitude'], business['coordinates']['longitude'])
            if self.check_distance(curr_distance) and business['id'] not in self.business_dict['id']:
                self.business_dict['id'].append(business['id'])
                self.business_dict['name'].append(business['name'])
                self.business_dict['latitude'].append(business['coordinates']['latitude'])
                self.business_dict['longitude'].append(business['coordinates']['longitude'])
                self.check_attribute('price', 'price', business)
                self.check_attribute('rating', 'rating', business)
                self.business_dict['url'].append(business['url'])
                offset_change += 1;

        self.num_businesses = len(self.business_dict['id'])
        self.search_offset += offset_change
        print(self.search_offset)


    def check_attribute(self, dict_key, api_key, api_entry):
        """Checks if given key in API returned data - mainly for price and rating scores"""
        if dict_key in api_entry:
            self.business_dict[dict_key].append(api_entry[api_key])
        else:
            self.business_dict[dict_key].append('N/A')

    def check_distance(self, dist):
        """Checks if location is within the specified radius"""
        return dist <= self.radius / 1000

    def batch_yelp_search(self):
        """Runs multiple Yelp API Queries up to a specified maximum"""
        while self.search_count < yelpQuery.max_searches:
            print("ITER")
            self.yelp_search()
            self.businesses = json.loads(self.req.text)
            if 'businesses' in self.businesses:
                self.parse_businesses()
                self.search_count += 1
            else:
                break

    def make_list(self):
        """Creates a nested list of attributes where each sublist is the attribute set for an individual business"""
        self.detail_list = []
        for index in range(0, self.num_businesses):
            curr_list = [self.business_dict['name'][index]]
            curr_list.append(self.business_dict['url'][index])
            curr_list.append(self.calc_distance(self.business_dict['latitude'][index], self.business_dict['longitude'][index]))
            curr_list.append(self.business_dict['rating'][index])
            curr_list.append(self.business_dict['price'][index])
            self.detail_list.append(curr_list)

        self.detail_list.sort(key = lambda x: x[2])

    def calc_distance(self, lat1, lon1):
        """Calculates the distance between search point and a business location in kilometers"""
        dist_degrees = pow(add(pow(self.latitude - lat1, 2), pow(self.longitude - lon1, 2)), 0.5)
        return round(dist_degrees * 111.139, 2)

    def set_radius(self, new_radius):
        yelpQuery.radius = new_radius

    def writeJSON_direct(self):
        features = []
        for index in range(self.num_businesses):
            features.append(
                Feature(
                    geometry = Point((float(self.business_dict['longitude'][index]), float(self.business_dict['latitude'][index]))),
                    properties = {
                        'name': self.business_dict['name'][index],
                        'rating': self.business_dict['rating'][index],
                        'price': self.business_dict['price'][index],
                        'url': self.business_dict['url'][index],
                    }
                )
            )
        self.collection = FeatureCollection(features)
        self.json_file = json.dumps(self.collection)

lat = 0
lon = 0

yq = None

app = Flask(__name__)


@app.route('/map')
def map():
    """Page with open businesses near user location"""
    global yq
    yq = yelpQuery(lat, lon, int(time.time()))
    yq.yelp_main()
    print(datetime.fromtimestamp(yq.time))
    return render_template('index.html', data = yq.json_file, latitude = yq.latitude, longitude = yq.longitude, businesses_list = yq.detail_list)

@app.route('/')
def location():
    """Homepage with prompt for user location and general information"""
    return render_template('location.html')

@app.route('/postmethod', methods = ['POST'])
def postmethod():
    """Handles POST requests for location data"""
    data = request.get_json()
    global lat, lon
    lat = data['location']['lat']
    lon = data['location']['lon']
    print(lat, lon)
    return jsonify(data)

@app.route('/customized', methods = ['GET'])
def get_method():
    """Handles GET requests for map modification"""
    yq.set_radius(int(request.args.get("distanceSelect")))
    return redirect('/map')
