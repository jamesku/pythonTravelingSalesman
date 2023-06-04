# @author James Kuhr
# @student ID: 01101396

import csv
import re

from HashTable import HashTable
from Package import Package
from Location import Location
from Truck import Truck
from datetime import datetime, time, timedelta

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
    condition = package_list[l][7]
    status = "at the hub"
    p = Package(idn, address, city, state, zipcode, deadline, mass, condition, status)
    packagehashtable.insertorupdate(p, idn)

# create our truck instances
truck2run1=Truck([], [], "HUB", 84107, 0.0)
truck1run1=Truck([], [], "HUB", 84107, 0.0)
truck2run2=Truck([], [], "HUB", 84107, 0.0)
truck1run2=Truck([], [], "HUB", 84107, 0.0)
truckthree=Truck([], [], "HUB", 84107, 0.0)

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



# for i in range(len(packagehashtable.table)):
#     pack = packagehashtable.lookup(i)
#     if pack is not None and pack.condition == "truck2":
#         truck2run2.packages.append([pack])

def updatepackagearrivaltimes(starttime, deliverymileage, packageindex, package_to_deliver):
        time_at_arrival = datetime.combine(datetime.today(), starttime) + timedelta(minutes=(int(deliverymileage) / 18) * 60)
        package_to_deliver.arrival = time_at_arrival.time().strftime('%I:%M:%S %p')
        package_to_deliver.departure = starttime.strftime('%I:%M:%S %p')
        packagehashtable.insertorupdate(package_to_deliver, packageindex)

total_together_count = 0
together_count = 0
for o in range(len(packagehashtable.table)):
    package_to_deliver = packagehashtable.lookup(o)
    if package_to_deliver is not None:
        if package_to_deliver.condition == "together":
            together_count += 1

total_truck2_count = 0
for o in range(len(packagehashtable.table)):
    package_to_deliver = packagehashtable.lookup(o)
    if package_to_deliver is not None:
        if package_to_deliver.condition == "truck2":
            total_truck2_count += 1

total_early_count = 0
early_count = 0
for o in range(len(packagehashtable.table)):
    package_to_deliver = packagehashtable.lookup(o)
    if package_to_deliver is not None:
        if package_to_deliver.deadline == "10:30 AM" or package_to_deliver.deadline == "9:00 AM":
            total_early_count += 1

total_905_count = 0
now905_count = 0
for o in range(len(packagehashtable.table)):
    package_to_deliver = packagehashtable.lookup(o)
    if package_to_deliver is not None:
        if package_to_deliver.condition == "now905":
            total_905_count += 1

total_wrong_count = 1
total_to_deliver = len(package_list)

truck2run1.starttime = time(8, 00)

#we run a special route on truck 2 for all the packages that must be delivered together, they are all on time and can be delivered in one round
while len(truck2run1.packages) < together_count:
    packagefound = False
    for m in range(len(locations_table)):
        if locations_table[m].address == truck2run1.address and int(locations_table[m].zipcode) == truck2run1.zipcode:
                for n in range(len(locations_table[m].distance_array)):
                    next_location_zipcode = locations_table[m].distance_array[n][1]
                    next_location_address = locations_table[m].distance_array[n][2]
                    distance_to_next_location = locations_table[m].distance_array[n][0]
                    for o in range(len(packagehashtable.table)):
                        package_to_deliver = packagehashtable.lookup(o)
                        if package_to_deliver is not None \
                                and len(truck2run1.packages) < together_count \
                                and package_to_deliver.status == "at the hub"\
                                and package_to_deliver.condition == "together":
                            if package_to_deliver.address == next_location_address and int(package_to_deliver.zipcode) == next_location_zipcode:
                                truck2run1.packages.append(package_to_deliver.idn)
                                if packagefound == False:
                                    truck2run1.mileage.append(float(distance_to_next_location))
                                    truck2run1.totalmileage = truck2run1.totalmileage + distance_to_next_location
                                else:
                                    truck2run1.mileage.append(0)
                                if package_to_deliver.deadline == "10:30 AM" or package_to_deliver.deadline == "9:00 AM":
                                    total_early_count -= 1
                                updatepackagearrivaltimes(truck2run1.starttime, truck2run1.totalmileage, o, package_to_deliver)
                                total_to_deliver -=1
                                package_to_deliver.status = "en route"
                                package_to_deliver.truck = "one"
                                package_to_deliver.departure = truck2run1.starttime
                                packagehashtable.insertorupdate(package_to_deliver, o)
                                packagefound = True
                                truck2run1.address = next_location_address
                                truck2run1.zipcode = next_location_zipcode
                    if packagefound:
                        break
                if packagefound:
                    break
        if packagefound:
            break

#this sends truck 2 back to the depot
for m in range(len(locations_table)):
    if truck2run1.address == locations_table[m].address and truck2run1.zipcode == int(locations_table[m].zipcode):
        for n in range(len(locations_table[m].distance_array)):
            if locations_table[m].distance_array[n][2] == "HUB":
                truck2run1.mileage.append(locations_table[m].distance_array[n][0])

#caluclate what time truck 2 returns
truck2run1_end_time = datetime.combine(datetime.today(), truck2run1.starttime) + timedelta(minutes = (int(truck2run1.totalmileage) / 18) * 60)
truck2run1.endtime = truck2run1_end_time.time()


# run a regular route on truck 1 and exclude any packages that have special conditions, except for early delivery
truck1run1.starttime = time(8, 00)
while len(truck1run1.packages) < 16 and len(truck1run1.packages) < total_to_deliver-total_wrong_count-total_905_count-total_truck2_count:
    packagefound = False
    for m in range(len(locations_table)):
        if locations_table[m].address == truck1run1.address and int(locations_table[m].zipcode) == truck1run1.zipcode:
                for n in range(len(locations_table[m].distance_array)):
                    next_location_zipcode = locations_table[m].distance_array[n][1]
                    next_location_address = locations_table[m].distance_array[n][2]
                    distance_to_next_location = locations_table[m].distance_array[n][0]
                    for o in range(len(packagehashtable.table)):
                        package_to_deliver = packagehashtable.lookup(o)
                        if package_to_deliver is not None \
                                and len(truck1run1.packages) < 16 \
                                and package_to_deliver.status == "at the hub"\
                                and package_to_deliver.condition != "now905" \
                                and package_to_deliver.condition != "truck2"\
                                and package_to_deliver.condition != "wrong":
                            if package_to_deliver.address == next_location_address and int(package_to_deliver.zipcode) == next_location_zipcode:
                                truck1run1.packages.append(package_to_deliver.idn)
                                if packagefound == False:
                                    truck1run1.mileage.append(float(distance_to_next_location))
                                    truck1run1.totalmileage = truck1run1.totalmileage + distance_to_next_location
                                else:
                                    truck1run1.mileage.append(0)
                                updatepackagearrivaltimes(truck1run1.starttime, truck1run1.totalmileage, o, package_to_deliver)
                                total_to_deliver -= 1
                                if package_to_deliver.deadline == "10:30 AM" or package_to_deliver.deadline == "9:00 AM":
                                    total_early_count -= 1
                                package_to_deliver.status = "en route"
                                package_to_deliver.truck = "one"
                                package_to_deliver.departure = truck1run1.starttime
                                packagehashtable.insertorupdate(package_to_deliver, o)
                                packagefound = True
                                truck1run1.address = next_location_address
                                truck1run1.zipcode = next_location_zipcode
                    if packagefound:
                        break
                if packagefound:
                    break
        if packagefound:
            break

#return truck 1 to the HUB
for m in range(len(locations_table)):
    if truck1run1.address == locations_table[m].address and truck1run1.zipcode == int(locations_table[m].zipcode):
        for n in range(len(locations_table[m].distance_array)):
            if locations_table[m].distance_array[n][2] == "HUB":
                truck1run1.mileage.append(locations_table[m].distance_array[n][0])

#calculate the end time for truck 1 first trip
truck1run1_end_time = datetime.combine(datetime.today(), truck1run1.starttime) + timedelta(minutes = (int(truck1run1.totalmileage) / 18) * 60)
truck1run1.endtime = truck1run1_end_time.time()

#we run truck two on a normal route, starting at 9:05, except for the package with the wrong address,
# which has to go out in the last truck or any packages that have to be delivered by 10:30.
if truck2run1.endtime > time(9,5):
    truck2run2.starttime = truck2run1.endtime
else:
    truck2run2.starttime = time(9, 5)

backtothehub = 0
while len(truck2run2.packages) < 16 and len(truck2run2.packages) < total_to_deliver-total_wrong_count-total_early_count:
    packagefound = False
    for m in range(len(locations_table)):
        if locations_table[m].address == truck2run2.address and int(locations_table[m].zipcode) == truck2run2.zipcode:
                for n in range(len(locations_table[m].distance_array)):
                    next_location_zipcode = locations_table[m].distance_array[n][1]
                    next_location_address = locations_table[m].distance_array[n][2]
                    distance_to_next_location = locations_table[m].distance_array[n][0]
                    for o in range(len(packagehashtable.table)):
                        package_to_deliver = packagehashtable.lookup(o)
                        if package_to_deliver is not None and len(truck2run2.packages) < 16 and package_to_deliver.status == "at the hub" \
                                and package_to_deliver.deadline != "10:30 AM" and package_to_deliver.condition != "wrong":
                            if package_to_deliver.address == next_location_address and int(package_to_deliver.zipcode) == next_location_zipcode:
                                truck2run2.packages.append(package_to_deliver.idn)
                                if packagefound == False:
                                    truck2run2.mileage.append(float(distance_to_next_location))
                                    truck2run2.totalmileage = truck2run2.totalmileage + distance_to_next_location
                                else:
                                    truck2run2.mileage.append(0)
                                updatepackagearrivaltimes(truck2run2.starttime, truck2run2.totalmileage, o, package_to_deliver)
                                package_to_deliver.status = "en route"
                                package_to_deliver.truck = "two"
                                package_to_deliver.departure = truck2run2.starttime
                                packagehashtable.insertorupdate(package_to_deliver, o)
                                packagefound = True
                                truck2run2.address = next_location_address
                                truck2run2.zipcode = next_location_zipcode
                    if packagefound:
                        break
                if packagefound:
                    break
        if packagefound:
            break

for m in range(len(locations_table)):
    if truck2run2.address == locations_table[m].address and truck2run2.zipcode == int(locations_table[m].zipcode):
        for n in range(len(locations_table[m].distance_array)):
            if locations_table[m].distance_array[n][2] == "HUB":
                truck2run2.mileage.append(locations_table[m].distance_array[n][0])


new_time = datetime.combine(datetime.today(), truck2run2.starttime) + timedelta(minutes = (int(truck2run2.totalmileage) / 18) * 60)
truck2run2.endtime = new_time.time()



#we run truck one on an express route, starting at 9:05, except for the package with the wrong address,
# which has to go out in the last truck or any packages that have to be delivered by 10:30.
if truck1run1.endtime > time(9, 5):
    truck1run2.starttime = truck2run1.endtime
else:
    truck1run2.starttime = time(9, 5)
backtothehub = 0

while len(truck1run2.packages) < 16 and len(truck1run2.packages) < total_early_count:
    packagefound = False
    for m in range(len(locations_table)):
        if locations_table[m].address == truck1run2.address and int(locations_table[m].zipcode) == truck1run2.zipcode:
                for n in range(len(locations_table[m].distance_array)):
                    next_location_zipcode = locations_table[m].distance_array[n][1]
                    next_location_address = locations_table[m].distance_array[n][2]
                    distance_to_next_location = locations_table[m].distance_array[n][0]
                    for o in range(len(packagehashtable.table)):
                        package_to_deliver = packagehashtable.lookup(o)
                        if package_to_deliver is not None and len(truck1run2.packages) < 16 and package_to_deliver.status == "at the hub" \
                                and package_to_deliver.deadline == "10:30 AM" and package_to_deliver.condition != "wrong":
                            if package_to_deliver.address == next_location_address and int(package_to_deliver.zipcode) == next_location_zipcode:
                                truck1run2.packages.append(package_to_deliver.idn)
                                if packagefound == False:
                                    truck1run2.mileage.append(float(distance_to_next_location))
                                    truck1run2.totalmileage = truck1run2.totalmileage + distance_to_next_location
                                else:
                                    truck1run2.mileage.append(0)
                                updatepackagearrivaltimes(truck1run2.starttime, truck1run2.totalmileage, o, package_to_deliver)
                                package_to_deliver.status = "en route"
                                package_to_deliver.truck = "two"
                                package_to_deliver.departure = truck1run2.starttime
                                packagehashtable.insertorupdate(package_to_deliver, o)
                                packagefound = True
                                truck1run2.address = next_location_address
                                truck1run2.zipcode = next_location_zipcode
                    if packagefound:
                        break
                if packagefound:
                    break
        if packagefound:
            break

for m in range(len(locations_table)):
    if truck1run2.address == locations_table[m].address and truck1run2.zipcode == int(locations_table[m].zipcode):
        for n in range(len(locations_table[m].distance_array)):
            if locations_table[m].distance_array[n][2] == "HUB":
                truck1run2.mileage.append(locations_table[m].distance_array[n][0])


new_time = datetime.combine(datetime.today(), truck1run2.starttime) + timedelta(minutes = (int(truck1run2.totalmileage) / 18) * 60)
truck1run2.endtime = new_time.time()

#for the last truck, we know it will run after the 11:08 package change. lets use truck 3 for this one. it will start after one
#of the drivers gets back
if truck2run2.endtime<truck1run2.endtime:
    starttime = truck2run2.starttime
else:
    starttime = truck1run2.starttime

if starttime < time(10, 20):
    starttime = time(10, 20)

truckthree.starttime = starttime

package_to_correct = packagehashtable.lookup(9)
package_to_correct.address = "410 S State St"
package_to_correct.zipcode = "84111"
packagehashtable.insertorupdate(package_to_correct, 9)

while len(truckthree.packages) < 16 and len(truck2run1.packages)+len(truckthree.packages)+len(truck1run1.packages)+len(truck2run2.packages)+len(truck1run2.packages) < len(package_list):
    packagefound = False
    for m in range(len(locations_table)):
        if locations_table[m].address == truckthree.address and int(locations_table[m].zipcode) == truckthree.zipcode:
                for n in range(len(locations_table[m].distance_array)):
                    next_location_zipcode = locations_table[m].distance_array[n][1]
                    next_location_address = locations_table[m].distance_array[n][2]
                    distance_to_next_location = locations_table[m].distance_array[n][0]
                    for o in range(len(packagehashtable.table)):
                        package_to_deliver = packagehashtable.lookup(o)
                        if package_to_deliver is not None and len(truckthree.packages) < 16 and package_to_deliver.status == "at the hub":
                            if package_to_deliver.address == next_location_address and int(package_to_deliver.zipcode) == next_location_zipcode:
                                truckthree.packages.append(package_to_deliver.idn)
                                if packagefound == False:
                                    truckthree.mileage.append(float(distance_to_next_location))
                                    truckthree.totalmileage = truckthree.totalmileage + distance_to_next_location
                                else:
                                    truckthree.mileage.append(0)
                                updatepackagearrivaltimes(truckthree.starttime, truck1run1.totalmileage, o, package_to_deliver)
                                package_to_deliver.status = "en route"
                                package_to_deliver.truck = "two, second trip"
                                package_to_deliver.departure = truckthree.starttime
                                packagehashtable.insertorupdate(package_to_deliver, o)
                                packagefound = True
                                truckthree.address = next_location_address
                                truckthree.zipcode = next_location_zipcode
                    if packagefound:
                        break
                if packagefound:
                    break
        if packagefound:
            break


for m in range(len(locations_table)):
    if truckthree.address == locations_table[m].address and truckthree.zipcode == int(locations_table[m].zipcode):
        for n in range(len(locations_table[m].distance_array)):
            if locations_table[m].distance_array[n][2] == "HUB":
                truckthree.mileage.append(locations_table[m].distance_array[n][0])

new_time = datetime.combine(datetime.today(), starttime) + timedelta(minutes = (int(truckthree.totalmileage) / 18) * 60)
truckthree.endtime = new_time.time()


print("Western Governors University Parcel Service (WGUPS) Package Tracking Program - Daily Truck Routing Complete")
print("Truck 2 made its 1st trip, leaving at "+str(truck2run1.starttime)+" and returning to the Hub at "+str(truck2run1.endtime)+
      "am, running a total of "+str(round(truck2run1.totalmileage,2))+" miles")
print("Truck 1 made its 1st trip, leaving at "+str(truck1run1.starttime)+" and returning to the Hub at "+str(truck1run1.endtime)+
      "am, running a total of "+str(round(truck1run1.totalmileage,2))+" miles")
print("Truck 2 made its 2nd trip, leaving at "+str(truck2run2.starttime)+" and returning to the Hub at "+str(truck2run2.endtime)+
      "am, running a total of "+str(round(truck2run2.totalmileage,2))+" miles")
print("Truck 1 made its 2nd trip, leaving at "+str(truck1run2.starttime)+" am and returning to the Hub at "+str(truck1run2.endtime)+
      "am, running a total of "+str(round(truck1run2.totalmileage,2))+" miles")
print("Truck 3 made its 1st trip, leaving at "+str(truckthree.starttime)+" am and returning to the Hub at "+str(truck1run2.endtime)+
      "am, running a total of "+str(round(truckthree.totalmileage,2))+" miles")
print("a total of "+str(round(truck2run1.totalmileage+truck1run1.totalmileage+truck2run2.totalmileage+
                              truck1run2.totalmileage+truckthree.totalmileage,2))+" miles was run today")

for i in range(len(packagehashtable.table)):
    if packagehashtable.lookup(i) is not None:
        this_package = packagehashtable.lookup(i)
        # print("Package ID: "+str(this_package.idn)+"\n""Address: "+this_package.address+"\nCity: "+this_package.city+
        #       "\nZipcode: "+str(this_package.zipcode)+"\nDeadline: "+this_package.deadline+"\nMass (kilos): "+this_package.mass+
        #       "\nCondition: "+this_package.condition+"\nStatus: "+this_package.status+"\nArrival: "+this_package.arrival+"\n")

        if this_package.deadline < this_package.arrival:
            print("Arrived after Deadline")
        if this_package.truck == "one" and this_package.condition == "truck2":
            print("Arrived in wrong truck")
        if this_package.truck != "one" and this_package.condition == "together":
            print("Arrived in wrong grouping")
        print("ID: "+str(this_package.idn)+", Address: "+this_package.address+", Deadline: "+this_package.deadline+
              ", Condition: "+this_package.condition+", Status: "+this_package.status+", Start Time: "+str(this_package.departure)+
              ", Arrival: "+this_package.arrival+
              ", Truck: "+this_package.truck+"\n")
