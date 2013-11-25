#In order for this code to work you have to
#run the command below
#sudo pip install pygeocoder
#
#once you do this this code should work as expected.

#!/usr/bin/python
from pygeocoder import Geocoder

home = raw_input("Enter your starting address: ")
end =  raw_input("Enter your end address: ")
results = Geocoder.geocode(home)
results2 = Geocoder.geocode(end)
print(results[0].coordinates)
print(results2[0].coordinates)
