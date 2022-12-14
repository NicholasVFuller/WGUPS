class Package:
    """A Package object consists of data such as package ID and delivery address."""

    # Only create a package with all data, no blank / "null" packages allowed.
    def __init__(self, package_id, delivery_address, delivery_deadline, delivery_city,
                 delivery_zip, delivery_weight, special_notes, delivery_status):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.delivery_weight = delivery_weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.delivery_address, self.delivery_deadline,
                                                   self.delivery_city, self.delivery_zip, self.delivery_weight,
                                                   self.special_notes, self.delivery_status)