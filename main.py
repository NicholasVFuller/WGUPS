# Nicholas Fuller 001081254
import route


def main():
    """Run the WGUPSDLDSDS program."""

    print("\n\nHello! Welcome to the WGUPS Daily Local Deliveries Supervisor Database System, or DLDSDS!\n\n" +
          "How can I assist you? Please type the number of a selection below:\n\n" +
          "1) View Package Status and Info\n" +
          "2) View Total Mileage Traveled by all Trucks\n\n")

    selection = input().strip()

    if selection == "1":
        print("\n\nPlease enter a time for the status and info of the package(s) below\n" +
              "(Military time only please! -> 1435 = 2:35PM or 2222 = 10:22PM):\n\n")
        time = input().strip()
        if not time.isdigit() or len(time) != 4:
            print("\n\nYou did not enter a valid 4 digit military time..." +
                  " The program will now terminate... Have a great day!")
            exit(1)
        time_int = int(time)
        if time_int < 0 or time_int > 2359 or time_int % 100 > 59:
            print("\n\nYou did not enter a valid 4 digit military time..." +
                  " The program will now terminate... Have a great day!")
            exit(1)

        chosen_time_route = route.Route(time_int)

        print("\n\nLook up the status and info of a single package, or all packages, during the given time?\n" +
              "Please type the number of a selection below:\n\n" +
              "1) Single Package Lookup\n" +
              "2) Lookup All Packages\n\n")
        selection = input().strip()

        if selection == "1":
            print("\n\nPlease enter a package ID to search for below:\n\n")
            selected_package_id = input().strip()

            if not selected_package_id.isdigit():
                print("\n\nYou did not enter a valid package ID (positive integer)... " +
                      "The program will now terminate... Have a great day!")
            if int(selected_package_id) < 1:
                print("\n\nYou did not enter a valid package ID (positive integer)... " +
                      "The program will now terminate... Have a great day!")

            chosen_package = chosen_time_route.packages.lookup(int(selected_package_id))

            if chosen_package is None:
                print("\n\nThe package ID you entered did not return a package from the search.\n\n" +
                      "The program will now terminate... Have a great day!")
            else:
                print("\n" + str(chosen_package) + "\n\nHere is the requested package data!\n" +
                      "Program will now terminate! Have a great day! Goodbye!")

        elif selection == "2":
            print("\n\nTruck 1 mileage: " + str(chosen_time_route.truck_1.get_mileage(chosen_time_route)) + "\n")
            print("Truck 2 mileage: " + str(chosen_time_route.truck_2.get_mileage(chosen_time_route)) + "\n")
            print("Truck 3 mileage: " + str(chosen_time_route.truck_3.get_mileage(chosen_time_route)) + "\n")
            print("Total mileage: " +
                  str(chosen_time_route.truck_1.get_mileage(chosen_time_route) +
                      chosen_time_route.truck_2.get_mileage(chosen_time_route) +
                      chosen_time_route.truck_3.get_mileage(chosen_time_route)) + "\n\n")
            print(chosen_time_route.packages)
            print("\n\nProgram will now terminate! Have a great day! Goodbye!")
            exit(0)
        else:
            print("\n\nYou did not enter a valid selection... The program will now terminate... Have a great day!")
    elif selection == "2":
        mileage_route = route.Route(2359)
        print("\n\nTruck 1 mileage: " + str(mileage_route.truck_1.get_mileage(mileage_route)) + "\n")
        print("Truck 2 mileage: " + str(mileage_route.truck_2.get_mileage(mileage_route)) + "\n")
        print("Truck 3 mileage: " + str(mileage_route.truck_3.get_mileage(mileage_route)) + "\n\n")

        print("Bringing the grand total mileage for the day to (drumroll please)...:     " +
              str(mileage_route.truck_1.get_mileage(mileage_route) +
                  mileage_route.truck_2.get_mileage(mileage_route) +
                  mileage_route.truck_3.get_mileage(mileage_route)) + "!!!\n\n")
        print("Program will now terminate! Have a great day! Goodbye!")
        exit(0)
    else:
        print("\n\nYou did not enter a valid selection... The program will now terminate... Have a great day!")


if __name__ == "__main__":
    main()