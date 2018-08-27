import requests
from DarkSkyAPI.DS_logger import logger

class BingGeoCode:

    base_url = "http://dev.virtualearth.net/REST/v1/Locations/?"

    def __init__(self, api_key, location, country:str=None):
        self.api_key = api_key
        self._data = None
        self._country = country
        self._location = location

    def _url_builder(self):
        if self.country:
            return self.base_url + "countryRegion={}&locality={}&key={}".format(
                self.country, self.location, self.api_key)
        else:
            return self.base_url + "locality={}&key={}".format(self.location, self.api_key)

    def _get_response(self):
        json_response = requests.get(self._url_builder()).json()
        dataset = json_response['resourceSets'][0]['resources']
        return dataset

    @property
    def has_multiple_results(self):
        return len(self.data) > 1

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
    def coords(self):
        logger.info(f"Setting coords for {self.data[0]['name']}")
        if self.has_multiple_results and not self.country:
            logger.warning(f"There are more than 1 locations called: {self.location}. Specify a country name as such:\n" 
                           f"GeoCode({self.api_key}, \"Amsterdam\", country=\"NL\")\n"
                           f"Location now set for {self.data[0]['name']}")
            logger.debug([name['name'] for name in self.data])
        if 'point' in self.data[0]:
            location = self.data[0]['point']['coordinates']
            coords = (location[0], location[1])
            return coords
        else:
            return None

    def __repr__(self):
        return "BingGeoCode({}, {})".format(self.api_key, self.location)

    def __str__(self):
        return f"Matching results: {len(self.data)}\n" \
               f"{[[l['address']['countryRegion'], l['address']['adminDistrict']] for l in self.data]}"