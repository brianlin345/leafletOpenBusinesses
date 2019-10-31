from flask import Flask, current_app, render_template, request, jsonify

import requests
import json, csv
import pandas as pd
from datetime import datetime
from geojson import Feature, FeatureCollection, Point, dump
import time



app = Flask(__name__)


class yelpQuery:
    yelp_url = "https://api.yelp.com/v3/businesses/search"
    api_key = "Ph5ToEVanaZhUmnCWJDAWFnlCah55sgnz3r91I-sC6ObZI8KCAyXDtI4cAqs7hoUg0GgquEJCnHhMBBoXfe6P2uPgafPpa5GkDLAGDtbeliu2JzileqOOHdPAN6zXXYx"
    business_keys = ['id', 'name', 'latitude', 'longitude', 'url']

    def __init__(self, lat, lon, time, radius = 1000, filename='businesses'):
        self.latitude = lat
        self.longitude = lon
        self.radius = radius
        self.time = time
        self.filename = filename
        self.headers = {'Authorization': 'Bearer %s' % yelpQuery.api_key}

    def yelp_main(self):
        self.yelp_search()
        self.parse_businesses()
        self.write_businesses()
        self.writeJSON()

    def yelp_search(self):
        self.params = {'latitude': self.latitude, 'longitude': self.longitude, 'radius': self.radius, 'open_at': self.time, 'limit': 50}
        self.req = requests.get(yelpQuery.yelp_url, params=self.params, headers= self.headers)
        if self.req.status_code == 200:
            return self.req
        else:
            print('JSON status code:{}'.format(self.req.status_code))

    def parse_businesses(self):
        self.business_dict = {business_key:[] for business_key in yelpQuery.business_keys}

        businesses = json.loads(self.req.text)
        businesses_parsed = businesses['businesses']

        for business in businesses_parsed:
            self.business_dict['id'].append(business['id'])
            self.business_dict['name'].append(business['name'])
            self.business_dict['latitude'].append(business['coordinates']['latitude'])
            self.business_dict['longitude'].append(business['coordinates']['longitude'])
            self.business_dict['url'].append(business['url'])

    def write_businesses(self):
        self.businesses_df = pd.DataFrame.from_dict(self.business_dict)
        self.businesses_df.to_csv('{}.csv'.format(self.filename), encoding='utf-8', index=False, header = False)
        print('File {0}{1} written successfully'.format(self.filename, '.csv'))

    def writeJSON(self):
        features = []
        with open('{}.csv'.format(self.filename), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for id, name, latitude, longitude, url in reader:
                latitude, longitude = map(float, (latitude, longitude))
                features.append(
                    Feature(
                        geometry = Point((longitude, latitude)),
                        properties = {
                            'name': name,
                            'url': url
                        }
                    )
                )

        self.collection = FeatureCollection(features)
        self.json_file = json.dumps(self.collection)

radius = 5000 # meters
lat = 0
lon = 0
#unix_time = 1571632240 # 6 pm Oct 26




@app.route('/postmethod', methods = ['POST'])
def postmethod():
    data = request.get_json()
    global lat, lon
    lat = data['location']['lat']
    lon = data['location']['lon']
    print(lat, lon)
    return jsonify(data)


@app.route('/map')
def index():
    yq = yelpQuery(lat, lon, int(time.time()), radius)
    yq.yelp_main()
    print(datetime.fromtimestamp(yq.time))
    print(yq.businesses_df)
    return render_template('index.html', data = yq.json_file, latitude = yq.latitude, longitude = yq.longitude)


@app.route('/list')
def lst():
    yq = yelpQuery(lat, lon, int(time.time()), radius)
    yq.yelp_main()
    return render_template('list.html', businesses = yq.business_dict['name'])


@app.route('/')
def location():
    return render_template('location.html')