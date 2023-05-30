# @author James Kuhr
# @student ID: 01101396

import csv
import datetime
import re

from HashTable import HashTable
from Package import Package
from Location import Location
from Truck import Truck

# Read the file of distance information
with open("resources/Distances.csv") as csvfile:
    distance_info = csv.reader(csvfile)
    distance_list = list(distance_info)

# format received CSV data into two arrays that can be combined with furter logic
locationsindex = []
for i in range(len(distance_list[0])):
    locationsindex.append(distance_list[0][i])
distance_list.pop(0)
locations_table = []
zip_isolator = r"\((\d{5})\)"

# combine arrays to get an array of objects that have their address, their zip code and an
# array of all locations, with their address, zip and distance from the top line location,
# sorted so that the nearest location is first in the list, setting up the greedy search pattern
for j in range(len(distance_list)):
    temparray = []
    mainzip = re.search(zip_isolator, locationsindex[j+1]).group(1)
    mainaddress = locationsindex[j+1][1:-8]
    for k in range(len(distance_list[j])):
        if locationsindex[k]:
            zipcode = int(re.search(zip_isolator, locationsindex[k]).group(1))
            address = locationsindex[k][1:-8]
            temparray.append([float(distance_list[j][k]), zipcode, address])
            temparray.sort()
    LocObj = Location(mainaddress, mainzip, temparray)
    locations_table.append(LocObj)

# import CSV with package information
with open("resources/Packages.csv") as csvfile:
    package_info = csv.reader(csvfile)
    package_list = list(package_info)
    print(package_list)

packagehashtable = HashTable()
# create package objects and insert into the hash table
for l in range(len(package_list)):
    idn = int(package_list[l][0])
    address = package_list[l][1]
    city = package_list[l][2]
    state = package_list[l][3]
    zipcode = int(package_list[l][4])
    deadline = package_list[l][5]
    mass = package_list[l][6]
    conditions = package_list[l][7]
    status = "at the hub"
    p = Package(idn, address, city, state, zipcode, deadline, mass, conditions, status)
    packagehashtable.insertorupdate(p, idn)

# create our truck instances
truckone=Truck(0, [], "HUB", 84107)
trucktwo=Truck(0, [], "HUB", 84107)

# we are going to use greedy sorting and sort packages into one truck at a time. The truck will
# use the locations_table to determine the location closest to its current location. It will
# then check if a package needs to be dropped off at that location. It will also check any conditions
# on that package that may modify how it travels. If it finds a match, it will add the package, and
# use the locations_table to determine where the next nearest delivery is.  Notably, this may be the
# same location its currently at.  If it does not find a package to deliver to the nearest location
# it will look at the second nearest location.  It will compare this to if it were to go to the
# nearest location and then a second location...
# Delivery times and total mileage will be calculated as locations are selected
# Urgent delivery times will be calculated

for m in range(len(locations_table)):
    if locations_table[m].address == truckone.address & int(locations_table[m].zipcode) == truckone.zipcode:
        for n in range(len(locations_table[n])):
            next_location_zipcode = locations_table[m][n][1]
            next_location_address = locations_table[m][n][2]
            for o in range(len(packagehashtable)):
                package_to_deliver = packagehashtable.lookup(o)
                if package_to_deliver.address == truckone.address & int(package_to_deliver.zipcode) == truckone.zipcode:
                    truckone.packages.append(o)


