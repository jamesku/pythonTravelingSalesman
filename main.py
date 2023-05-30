# @author James Kuhr

import csv
import datetime
import re

from HashTable import HashTable
from Package import Package
from Location import Location

# Read the file of distance information
with open("resources/Distances.csv") as csvfile:
    distance_info = csv.reader(csvfile)
    distance_list = list(distance_info)

# format received CSV data into two arrays that can be combined with furter logic
locationsindex = []
for i in range(len(distance_list[0])):
    locationsindex.append(distance_list[0][i])
distance_list.pop(0)
locationstablearray = []
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
            zipcode = re.search(zip_isolator, locationsindex[k]).group(1)
            address = locationsindex[k][1:-8]
            temparray.append([float(distance_list[j][k]), zipcode, address])
            temparray.sort()
    LocObj = Location(mainaddress, mainzip, temparray)
    locationstablearray.append(LocObj)

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
    zipcode = package_list[l][4]
    deadline = package_list[l][5]
    mass = package_list[l][6]
    conditions = package_list[l][7]
    status = "at the hub"
    p = Package(idn, address, city, state, zipcode, deadline, mass, conditions, status)
    packagehashtable.insertorupdate(p, idn)