# HashTable constructor with no capacity specified
class HashTable:

    def __init__(self):
        self.table = []

        # Number of buckets is defined for performance improvement.
        tl = 61

        # build the hashtable to the specified length
        for i in range(tl):
            self.table.append([])

    # Insert a value or updates a value in the HashTable
    def insertorupdate(self, value, key):
        # uses the modulus of the integer key to find the index (bucket) in the array
        bucket = hash(key) % len(self.table)
        # reference the list of values in the bucket at that index
        blist = self.table[bucket]
        # iterate through the list and see if the value exists and replaces with new value if so
        # O(n) search time
        for k in blist:
            if key == k[0]:
                k[1] = value
            return True
        # if the key is not in the list append they key and value
        blist.append([key, value])
        return True

    # Lookup a value in the HashTable
    def lookup(self, key):
        # uses the modulus of the integer key to find the index (bucket) in the array
        bucket = hash(key) % len(self.table)
        # reference the list of values in the bucket at that index
        blist = self.table[bucket]
        # iterate through the list and see if the key exists and return the value if so
        # O(n) search time
        for k in blist:
            if key == k[0]:
                return k[1]
            return None

    # Lookup a value in the HashTable
    def remove(self, key):
        # uses the modulus of the integer key to find the index (bucket) in the array
        bucket = hash(key) % len(self.table)
        # reference the list of values in the bucket at that index
        blist = self.table[bucket]
        # iterate through the list and see if the key exists and delete the value if so
        # O(n) search time
        for k in blist:
            if k[0] == key:
                blist.remove([k[0], k[1]])
            return False
