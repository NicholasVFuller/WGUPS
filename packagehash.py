import csv
from copy import deepcopy
import package


class PackageHash:
    """A double hashing, self resizing hashtable for storing packages."""

    def __init__(self, initial_capacity=11):
        self.filled = 0
        self.h = 7
        self.capacity = 11

        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()

        self.table = [self.EMPTY_SINCE_START] * initial_capacity

    def h2(self, item):
        """Secondary hash function."""
        return self.h - hash(item) % self.h

    def insert(self, insert_package):
        """Insert a package into the hash table and resize the table if necessary."""
        for i in range(len(self.table)):
            bucket = (hash(insert_package.package_id) + self.h2(insert_package.package_id) * i) % len(self.table)
            if type(self.table[bucket]) is EmptyBucket:
                self.table[bucket] = insert_package
                self.filled += 1
                if self.filled / self.capacity > 0.7:
                    self.resize()
            return

    def lookup(self, package_id):
        """Return the package contained in the hash table with the specified package_id. If it is not in the 
           hash table, return None."""
        for i in range(len(self.table)):

            bucket = (hash(package_id) + self.h2(package_id) * i) % len(self.table)
            this_bucket = self.table[bucket]
            if isinstance(this_bucket, EmptyBucket):
                if this_bucket is self.EMPTY_SINCE_START:
                    return None
                continue
            assert isinstance(this_bucket, package.Package)
            if this_bucket.package_id == package_id:
                return self.table[bucket]

        return None

    def remove(self, package_id):
        """Remove the specified package if it exists."""
        for i in range(len(self.table)):
            bucket = (hash(package_id) + self.h2(package_id) * i) % len(self.table)
            this_bucket = self.table[bucket]
            if isinstance(this_bucket, EmptyBucket):
                if this_bucket is self.EMPTY_SINCE_START:
                    return
                continue
            assert isinstance(this_bucket, package.Package)
            if this_bucket.package_id == package_id:
                self.table[bucket] = self.EMPTY_AFTER_REMOVAL
                return
        return

    def resize(self):
        """Resize the hash table to a capacity of the next prime value."""
        self.filled = 0
        self.h = self.capacity
        self.capacity = next_prime(self.capacity)

        old_table = deepcopy(self.table)

        self.table = [self.EMPTY_SINCE_START] * self.capacity

        for i in range(len(old_table)):
            if isinstance(old_table[i], EmptyBucket):
                continue
            current_package = old_table[i]
            assert isinstance(current_package, package.Package)
            self.insert(current_package)

    def __str__(self):
        to_return = ""
        for p in self.table:
            if isinstance(p, EmptyBucket):
                continue
            to_return += str(p) + "\n"
        return to_return


class EmptyBucket:
    """Represent an empty bucket."""
    pass


def isprime(num: int):
    """Return True if num is a prime number, False otherwise."""
    if num < 2:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0:
        return False

    i = 3
    while i < num:
        if num % i == 0:
            return False
        i += 1

    return True


def next_prime(num: int):
    """Return the first prime number to occur after num."""
    if num < 2:
        return 2
    if num == 2:
        return 3
    if num % 2 == 0:
        num += 1
    else:
        num += 2

    while True:
        if isprime(num):
            return num
        num += 2


def load_package_data(filename):
    """Return a PackageHash object filled with packages created from data contained in a specified .csv file."""
    hashed_packages = PackageHash()
    with open(filename) as packages:
        package_data = csv.reader(packages, delimiter=',')
        for pkg in package_data:
            package_id = int(pkg[0])
            delivery_address = pkg[1]
            delivery_city = pkg[2] + ", " + pkg[3]
            delivery_zip = pkg[4]
            delivery_deadline = pkg[5]
            delivery_weight = pkg[6]
            special_notes = pkg[7]
            delivery_status = "error"

            this_package = package.Package(package_id, delivery_address, delivery_deadline, delivery_city, delivery_zip,
                                           delivery_weight, special_notes, delivery_status)

            hashed_packages.insert(this_package)
    return hashed_packages