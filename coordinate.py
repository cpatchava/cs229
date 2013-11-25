#!/usr/bin/python
from pygeocoder import Geocoder
results = Geocoder.geocode("10226 A Park Circle East Cupertino CA 95014")
print(results[0].coordinates)
