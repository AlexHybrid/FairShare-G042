class House:
    def __init__(self, house_id, location, rent):
        self.house_id = house_id
        self.location = location
        self.rent = rent
        self.is_rented = False

    def __str__(self):
        status = "Rented" if self.is_rented else "Available"
        return f"ID: {self.house_id} | Location: {self.location} | Rent: RM{self.rent} | Status: {status}"


class HouseRentalApp:
    def __init__(self):
        self.houses = []

    def add_house(self, house_id, location, rent):
        house = House(house_id, location, rent)
        self.houses.append(house)
        print("✅ House added successfully!")

    def view_houses(self):
        if not self.houses:
            print("No houses available.")
        else:
            for house in self.houses:
                print(house)

    def rent_house(self, house_id):
        for house in self.houses:
            if house.house_id == house_id:
                if not house.is_rented:
                    house.is_rented = True
                    print(f"🏡 House {house_id} rented successfully!")
                else:
                    print("❌ House already rented.")
                return
        print("❌ House not found.")

    def search_by_location(self, location):
        found = [house for house in self.houses if house.location.lower() == location.lower()]
        if found:
            for house in found:
                print(house)
        else:
            print("No houses found in that location.")


def main():
    app = HouseRentalApp()

    while True:
        print("\n--- House Renting App ---")
        print("1. Add House")
        print("2. View Houses")
        print("3. Rent House")
        print("4. Search by Location")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            house_id = input("Enter House ID: ")
            location = input("Enter Location: ")
            rent = float(input("Enter Rent: "))
            app.add_house(house_id, location, rent)

        elif choice == "2":
            app.view_houses()

        elif choice == "3":
            house_id = input("Enter House ID to rent: ")
            app.rent_house(house_id)

        elif choice == "4":
            location = input("Enter location to search: ")
            app.search_by_location(location)

        elif choice == "5":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
