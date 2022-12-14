import csv


class Addresses:
    """Create and store a dictionary of addresses for use with the distance matrix."""

    def __init__(self):
        self.addresses = load_address_data()

    def __str__(self):
        to_return = ""
        for a in self.addresses.keys():
            to_return += str(self.addresses[a]) + " " + a + "\n"
        return to_return


def load_address_data():
    """Return a dictionary filled with address data from 'WGUPS Distance Table.csv'"""
    to_return = {}
    with open("WGUPS Distance Table.csv") as addresses:
        address = csv.reader(addresses, delimiter=',')
        i = 0
        for a in address:
            cell = a[1].split("(")
            cell = cell[0].strip()
            to_return[cell] = i
            i += 1
        return to_return