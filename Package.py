# Package constructor

class Package:
    def __init__(self, idn, address, city, state, zipcode, deadline, mass, condition, status):
        self.idn = idn
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = mass
        self.condition = condition
        self.status = status
        self.arrival = None
        self.truck = None
        self.departure = None
        # self.priority = self.set_priority()

    @property
    def __str__(self):
        return "Package ID: {self.idn}\nAddress: {self.address}\nCity: {self.city}\nZipcode: {" \
               "self.zipcode}\nDeadline: {self.deadline}\nMass (kilos): {self.mass}\nCondition: {" \
               "self.condition}\nStatus: {self.status}\nArrival: {self.arrival}"
    #
    # def set_priority(self):
    #     if self.deadline == "9:00 AM":
    #         return 1
    #     if self.deadline == "10:30 AM":
    #         return 2
    #     if self.deadline == "EOD":
    #         return 3
    #     if self.condition == "together":
    #         return 1
    #     if self.condition == "wrong":
    #         return 4
