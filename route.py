import addresses
import distances
import math
import package
import packagehash


class Route:
    """Simulate the status of trucks and packages for the day at a given time(int between 0 and 2359)."""

    def __init__(self, time):
        self.time = time
        self.packages = packagehash.load_package_data("WGUPS Package File.csv")
        self.hub = packagehash.PackageHash()

        # fill hub with all packages
        for p in self.packages.table:
            if isinstance(p, packagehash.EmptyBucket):
                continue
            assert isinstance(p, package.Package)
            p.delivery_status = "at the hub"
            self.hub.insert(p)

        self.distances = distances.Distances()
        self.addresses = addresses.Addresses()

        self.truck_1 = Truck()
        self.truck_2 = Truck()
        self.truck_3 = Truck()

        self.plan_truck_routes()

    def distance_between(self, address_1, address_2):
        """Return the distance between address_1 and address_2."""
        address_table = self.addresses.addresses
        distance_table = self.distances.distance_data
        return distance_table[address_table[address_1]][address_table[address_2]]

    def plan_truck_routes(self):
        """Plan the truck routes for the day, load trucks, and ensure all packages are delivered on time with 
           truck mileage totaling less than 140 miles, while meeting all other constraints."""
        # Packages 13, 15, 19 must all be delivered from the same truck.
        deliver_together = [self.packages.lookup(13), self.packages.lookup(15), self.packages.lookup(19)]
        self.hub.remove(13)
        self.hub.remove(15)
        self.hub.remove(19)

        # Packages 6, 25, 28 and 32 (and 26 and 31 since they are going to same addresses) do not arrive until 0905.
        late_arrivals = [(self.packages.lookup(6)), self.packages.lookup(25), self.packages.lookup(26),
                         self.packages.lookup(28), self.packages.lookup(31), self.packages.lookup(32)]
        self.hub.remove(6)
        self.hub.remove(25)
        self.hub.remove(26)
        self.hub.remove(28)
        self.hub.remove(31)
        self.hub.remove(32)

        # Packages 3, 18, 36 and 38 must be on truck 2.
        truck_2_only = [self.packages.lookup(3), self.packages.lookup(18), self.packages.lookup(36),
                        self.packages.lookup(38)]
        self.hub.remove(3)
        self.hub.remove(18)
        self.hub.remove(36)
        self.hub.remove(38)

        # If the time is 10:20am or later, package 9's address can be updated.
        if self.time >= 1020:
            package_9 = self.packages.lookup(9)
            assert isinstance(package_9, package.Package)
            package_9.delivery_address = "410 S State St"
            package_9.delivery_city = "Salt Lake City, UT"
            package_9.delivery_zip = "84111"
            self.hub.remove(9)
        else:
            package_9 = self.packages.lookup(9)
            assert isinstance(package_9, package.Package)
            self.hub.remove(9)

        urgent_packages = []
        non_urgent_packages = []

        # Sort urgent packages and non-urgent packages into separate lists.
        for p in self.hub.table:
            if isinstance(p, packagehash.EmptyBucket):
                continue
            assert isinstance(p, package.Package)
            if p.delivery_deadline != "EOD":
                urgent_packages.append(self.packages.lookup(p.package_id))
                self.hub.remove(p.package_id)
            else:
                non_urgent_packages.append(self.packages.lookup(p.package_id))
                self.hub.remove(p.package_id)

        urgent_packages = self.two_opt(urgent_packages)

        truck_1_route_0 = []

        # Put 2/3 of the 2opted urgent packages onto truck 1 route 0.
        i = 0
        part = int(len(urgent_packages) * 2 / 3)
        while i < part:
            truck_1_route_0.append(self.packages.lookup(urgent_packages.pop(0).package_id))
            i += 1

        # Add the packages that must be delivered together(from the same truck) to the remaining urgent packages.
        urgent_packages.append(deliver_together[0])
        urgent_packages.append(deliver_together[1])
        urgent_packages.append(deliver_together[2])

        truck_2_route_0 = self.two_opt(urgent_packages)

        # Load trucks 1 and 2 and start delivering.
        for p in truck_1_route_0:
            self.truck_1.add_package_to_truck_route(p, 0)

        for p in truck_2_route_0:
            self.truck_2.add_package_to_truck_route(p, 0)

        self.truck_1.load_truck_and_start_driving(self, 800, 0)
        self.truck_2.load_truck_and_start_driving(self, 800, 0)

        return_time_1 = self.truck_1.get_return_time(self, 0)
        return_time_2 = self.truck_2.get_return_time(self, 0)

        late_arrivals = self.two_opt(late_arrivals)

        for p in late_arrivals:
            self.truck_3.add_package_to_truck_route(p, 0)

        # Begin delivering the late arrivals on truck 3 no earlier than 9:05AM.
        if return_time_1 < return_time_2:
            if return_time_1 < 905:
                self.truck_3.load_truck_and_start_driving(self, 905, 0)
            else:
                self.truck_3.load_truck_and_start_driving(self, return_time_1, 0)
            returned = 1
        else:
            if return_time_2 < 905:
                self.truck_3.load_truck_and_start_driving(self, 905, 0)
            else:
                self.truck_3.load_truck_and_start_driving(self, return_time_2, 0)
            returned = 2

        return_time_3 = self.truck_3.get_return_time(self, 0)

        non_urgent_packages = self.two_opt(non_urgent_packages)

        # Add the first half of the 2opted non-urgent packages to truck 2 with the packages only for truck 2.
        i = 0
        part = int(len(non_urgent_packages) / 2)
        while i < part:
            truck_2_only.append(non_urgent_packages.pop(0))
            i += 1

        # Add package 9(which needs its address updated) to truck 2.
        truck_2_only.append(package_9)

        truck_1_route_1 = self.two_opt(non_urgent_packages)

        truck_2_route_1 = self.two_opt(truck_2_only)

        # Load the final 2 trucks and start final deliveries.
        for p in truck_1_route_1:
            self.truck_1.add_package_to_truck_route(p, 1)
        for p in truck_2_route_1:
            self.truck_2.add_package_to_truck_route(p, 1)

        if returned == 1:
            self.truck_1.load_truck_and_start_driving(self, return_time_3, 1)
            if return_time_2 > 1020:
                self.truck_2.load_truck_and_start_driving(self, return_time_2, 1)
            else:
                self.truck_2.load_truck_and_start_driving(self, 1020, 1)
        else:
            self.truck_1.load_truck_and_start_driving(self, return_time_1, 1)
            if return_time_3 > 1020:
                self.truck_2.load_truck_and_start_driving(self, return_time_3, 1)
            else:
                self.truck_2.load_truck_and_start_driving(self, 1020, 1)

    def two_opt(self, route_to_sort):
        """Perform the 2opt heuristic algorithm on the passed in route. 
           Return a new route with optimized distance(lower)."""
        best_distance = self.calculate_total_distance(route_to_sort)
        old_best_distance = -1.0
        while not math.isclose(best_distance, old_best_distance):
            old_best_distance = best_distance
            returned = self.two_opt_loops(best_distance, route_to_sort)
            if returned is None:
                continue
            best_distance = returned[0]
            route_to_sort = returned[1]
        return route_to_sort

    def two_opt_loops(self, best_distance: float, existing_route: list[package.Package]):
        """Loop through the existing route and perform 2optswaps. 
           If a new best distance(lowest) and route are found, return them, otherwise return None."""
        i = 0
        while i < len(existing_route) - 1:
            k = i + 1
            while k < len(existing_route):
                new_route = two_opt_swap(existing_route, i, k)
                new_distance = self.calculate_total_distance(new_route)
                if new_distance < best_distance:
                    to_return = [new_distance, new_route]
                    return to_return
                k += 1
            i += 1

    def calculate_total_distance(self, route_to_calculate: list[package.Package]):
        """Return the total distance of the of a route traversed in order."""
        total_distance = 0
        for i in range(len(route_to_calculate)):
            if i == 0:
                total_distance += self.distance_between("HUB", route_to_calculate[i].delivery_address)
            if i == len(route_to_calculate) - 1:
                return total_distance + self.distance_between(route_to_calculate[i].delivery_address, "HUB")
            total_distance += self.distance_between(route_to_calculate[i].delivery_address,
                                                    route_to_calculate[i + 1].delivery_address)


class Truck:
    """A Truck contains routes that contain packages to be delivered in order, 
       as well as depart times for each route."""

    def __init__(self):
        self.routes = []
        self.depart_times = []

    def add_package_to_truck_route(self, this_package: package.Package, route_num: int):
        """Add passed in package to this truck's selected route number, create the route if needed."""
        if len(self.routes) < route_num or route_num < 0:
            print("\nError: Invalid truck route index. Program will terminate.")
            exit(1)
        if len(self.routes) == route_num:
            self.routes.append([this_package])
            self.depart_times.append(-1)
        else:
            if len(self.routes[route_num]) == 16:
                print("\nError: Cannot load more than 16 packages onto a truck. Program will terminate.")
                exit(1)
            self.routes[route_num].append(this_package)

    def load_truck_and_start_driving(self, this_route: Route, depart_time, route_num: int):
        """Set the depart time for this truck's selected route and change the status of all packages on that route 
           to 'en route'."""
        if len(self.routes) <= route_num or route_num < 0:
            print("\nError: Invalid truck route index. Program will terminate.")
            exit(1)
        self.depart_times[route_num] = depart_time
        if this_route.time >= depart_time:
            for p in self.routes[route_num]:
                p.delivery_status = "en route"

    def get_mileage(self, this_route: Route):
        """Return this truck's total mileage at this Route's specified time."""
        if len(self.routes) == 0:
            return 0
        mileage = 0
        current = 0
        while current < len(self.routes):
            depart_time = self.depart_times[current]
            if depart_time == -1 or this_route.time <= depart_time:
                mileage += 0
                current += 1
                continue
            return_time = self.get_return_time(this_route, current)
            if this_route.time < return_time:
                mileage += get_minutes_between(this_route.time, depart_time) * 0.3
                current += 1
                continue
            else:
                mileage += get_minutes_between(return_time, depart_time) * 0.3
                current += 1
                continue
        return mileage

    def get_return_time(self, this_route: Route, route_num: int):
        """Get the time that this truck returned to the HUB from this truck's the specified route number."""
        depart_time = self.depart_times[route_num]
        prev_address = ""
        current_truck_route = self.routes[route_num]
        miles = 0
        for i in range(len(current_truck_route) + 1):
            if i == 0:
                address_1 = "HUB"
            else:
                address_1 = prev_address
            if i == len(current_truck_route):
                address_2 = "HUB"
            else:
                address_2 = current_truck_route[i].delivery_address
            prev_address = address_2
            miles += this_route.distance_between(address_1, address_2)
            delivery_time = add_minutes_to_time(int(miles / 0.3), depart_time)
            if delivery_time <= this_route.time and i != len(current_truck_route):
                current_truck_route[i].delivery_status = "delivered " + str(delivery_time)

        return add_minutes_to_time(int(miles / 0.3), depart_time)


def get_minutes_between(greater_time, lesser_time):
    """Return minutes between a greater time(which is more than lesser_time) and a lesser time."""
    hours = int(greater_time / 100) - int(lesser_time / 100)
    greater_minutes = greater_time % 100
    lesser_minutes = lesser_time % 100

    if greater_minutes >= lesser_minutes:
        minutes = greater_minutes - lesser_minutes
    else:
        hours -= 1
        greater_minutes += 60
        minutes = greater_minutes - lesser_minutes

    return int(int(hours * 60) + int(minutes))


def add_minutes_to_time(minutes, time):
    """Add minutes(positive integer representing number of minutes to add) to time(int with a value of 0 to 2359)."""
    while minutes % 60 > 0 and minutes >= 60:
        minutes -= 60
        time += 100
    if time % 100 + minutes >= 60:
        time += 100
        minutes = (time % 100 + minutes) - 60
        return int(time / 100) * 100 + minutes
    else:
        return time + minutes


def two_opt_swap(current_route, i, k):
    """Return a new route where the region i through k of the current route is reversed."""
    new_route = []
    x = 0
    while x < i:
        new_route.append(current_route[x])
        x += 1
    y = k
    while y >= i:
        new_route.append(current_route[y])
        y -= 1
    k += 1
    while k < len(current_route):
        new_route.append(current_route[k])
        k += 1

    return new_route