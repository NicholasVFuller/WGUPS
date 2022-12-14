import csv


class Distances:
    """Create and store a distance matrix for use with addresses."""

    def __init__(self):
        self.distance_data = [[]]
        self.load_distance_data()

    def load_distance_data(self):
        """Load distance data from 'WGUPS Distance Table.csv' into distance_data matrix."""
        with open("WGUPS Distance Table.csv") as distances:
            distance = csv.reader(distances, delimiter=',')
            lines = 0
            for d in distance:
                lines += 1
            self.distance_data = [[-1.0] * lines for i in range(lines)]
            distances.seek(0)
            distance = csv.reader(distances, delimiter=',')
            j = 0
            for d in distance:
                i = 0
                b = 0
                for a in d:
                    if b < 2:
                        b += 1
                        continue
                    if a == "":
                        break
                    self.distance_data[i][j] = float(a)
                    self.distance_data[j][i] = float(a)
                    i += 1
                j += 1

    def __str__(self):
        to_return = ""
        for i in range(len(self.distance_data)):
            for j in range(len(self.distance_data)):
                to_return += str(self.distance_data[i][j]) + " "
            to_return += "\n\n"
        return to_return

    # returns True if the data in distance_data table is valid, returns false otherwise.
    def verify_data(self):
        """Double check that distance data import was successful. Return True if distance_data table is correct, 
           False otherwise."""
        with open("WGUPS Distance Table.csv") as distances:
            distance = csv.reader(distances, delimiter=',')
            j = 0
            for d in distance:
                i = 0
                a = 2
                while float(d[a]) != 0.0:
                    if self.distance_data[i][j] != float(d[a]) or self.distance_data[j][i] != float(d[a]):
                        return False
                    print("Added " + d[a] + " to [" + str(i) + "][" + str(j) + "] and [" + str(j) + "][" + str(i) + "]")
                    i += 1
                    a += 1
                if self.distance_data[i][j] != 0.0 or self.distance_data[j][i] != 0.0:
                    return False
                print("Added 0.0 " + "to [" + str(i) + "][" + str(j) + "] and [" + str(j) + "][" + str(i) + "]")
                j += 1
            return True