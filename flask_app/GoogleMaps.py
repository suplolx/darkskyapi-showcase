import requests
from DarkSkyAPI.DS_logger import logger

class GoogleGeoCode:

    base_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"

    def __init__(self, api_key, location):
        self.api_key = api_key
        self._data = None
        self._location = location

    def _url_builder(self):
        return self.base_url.format(self.location, self.api_key)

    def _get_response(self):
        json_response = requests.get(self._url_builder()).json()
        return json_response

    @property
    def data(self):
        return self._get_response()

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, val):
        self._country = val

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        self._location = val

    @property
    def admin_district_1(self):
        if self.data['results'][0]['address_components'][1]:
            return self.data['results'][0]['address_components'][1]
        else:
            return None

    @property
    def admin_district_2(self):
        if self.data['results'][0]['address_components'][2]:
            return self.data['results'][0]['address_components'][2]
        else:
            return None

    @property
    def coords(self):
        coords = (self.data['results'][0]['geometry']['location']['lat'], self.data['results'][0]['geometry']['location']['lng'])
        return coords

    def __repr__(self):
        return "GoogleGeoCode({}, {})".format(self.api_key, self.location)
