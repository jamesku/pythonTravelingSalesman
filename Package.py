# Package constructor
class Package:
    def __init__(self, idn, address, city, state, zipcode, deadline, mass, conditions, status):
        self.idn = idn
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = mass
        self.conditions = conditions
        self.status = status
        self.departure = None
        self.arrival = None

    @property
    def __str__(self):
        return f'{self.idn}'

