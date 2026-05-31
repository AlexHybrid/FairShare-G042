import os

# Utility function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Property:
    def __init__(self, property_id, address, rent_price):
        self.property_id = property_id
        self.address = address
        self.rent_price = rent_price
        self.tenant = None

    def assign_tenant(self, tenant):
        self.tenant = tenant

    def __str__(self):
        return f"Property {self.property_id}: {self.address} | Rent: RM{self.rent_price} | Tenant: {self.tenant.name if self.tenant else 'None'}"


class Tenant:
    def __init__(self, tenant_id, name, contact):
        self.tenant_id = tenant_id
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"Tenant {self.tenant_id}: {self.name} ({self.contact})"


class RentalAgreement:
    def __init__(self, property, tenant, start_date, end_date, deposit):
        self.property = property
        self.tenant = tenant
        self.start_date = start_date
        self.end_date = end_date
        self.deposit = deposit
        self.payments = []

    def add_payment(self, amount, date):
        self.payments.append({"amount": amount, "date": date})

    def __str__(self):
        return f"Agreement: {self.tenant.name} renting {self.property.address} from {self.start_date} to {self.end_date}"


class RentalSystem:
    def __init__(self):
        self.properties = []
        self.tenants = []
        self.agreements = []

    # 📌 Property Management
    def add_property(self):
        clear_screen()
        pid = len(self.properties) + 1
        address = input("Enter property address: ")
        try:
            rent = float(input("Enter monthly rent: RM"))
        except ValueError:
            print("❌ Rent must be a number!")
            return
        p = Property(pid, address, rent)
        self.properties.append(p)
        print("✅ Property added!")

    # 📌 Tenant Management
    def register_tenant(self):
        clear_screen()
        tid = len(self.tenants) + 1
        name = input("Enter tenant name: ")
        contact = input("Enter tenant contact: ")
        t = Tenant(tid, name, contact)
        self.tenants.append(t)
        print("✅ Tenant registered!")

    # 📌 Agreement Creation
    def create_agreement(self):
        clear_screen()
        if not self.properties or not self.tenants:
            print("⚠️ Add property and tenant first!")
            return

        self.list_properties()
        try:
            pid = int(input("Choose property ID: "))
            property = next((p for p in self.properties if p.property_id == pid), None)
            if not property:
                print("❌ Invalid property ID!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return

        self.list_tenants()
        try:
            tid = int(input("Choose tenant ID: "))
            tenant = next((t for t in self.tenants if t.tenant_id == tid), None)
            if not tenant:
                print("❌ Invalid tenant ID!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return

        start = input("Enter start date (YYYY-MM-DD): ")
        end = input("Enter end date (YYYY-MM-DD): ")
        try:
            deposit = float(input("Enter deposit amount: RM"))
        except ValueError:
            print("❌ Deposit must be a number!")
            return

        agreement = RentalAgreement(property, tenant, start, end, deposit)
        self.agreements.append(agreement)
        property.assign_tenant(tenant)
        print("✅ Agreement created!")

    # 📌 Payment Tracking
    def record_payment(self):
        clear_screen()
        if not self.agreements:
            print("⚠️ No agreements found!")
            return

        self.list_agreements()
        try:
            aid = int(input("Choose agreement number (1..N): "))
            agreement = self.agreements[aid-1]
        except (ValueError, IndexError):
            print("❌ Invalid agreement selection!")
            return

        try:
            amount = float(input("Enter payment amount: RM"))
        except ValueError:
            print("❌ Payment must be a number!")
            return

        date = input("Enter payment date (YYYY-MM-DD): ")
        agreement.add_payment(amount, date)
        print("✅ Payment recorded!")

    # 📌 Listing with pause
    def list_properties(self):
        clear_screen()
        if not self.properties:
            print("⚠️ No properties available.")
        else:
            for p in self.properties:
                print(p)
        input("\nPress Enter to return to menu...")

    def list_tenants(self):
        clear_screen()
        if not self.tenants:
            print("⚠️ No tenants registered.")
        else:
            for t in self.tenants:
                print(t)
        input("\nPress Enter to return to menu...")

    def list_agreements(self):
        clear_screen()
        if not self.agreements:
            print("⚠️ No agreements created.")
        else:
            for i, a in enumerate(self.agreements, start=1):
                print(f"{i}. {a}")
                if a.payments:
                    print("   Payments:")
                    for pay in a.payments:
                        print(f"     - RM{pay['amount']} on {pay['date']}")
        input("\nPress Enter to return to menu...")


# 🚀 Menu-driven program
if __name__ == "__main__":
    system = RentalSystem()

    while True:
        clear_screen()
        print("\n--- Rental System Menu ---")
        print("1. Add Property")
        print("2. Register Tenant")
        print("3. Create Agreement")
        print("4. Record Payment")
        print("5. List Properties")
        print("6. List Tenants")
        print("7. List Agreements")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            system.add_property()
        elif choice == "2":
            system.register_tenant()
        elif choice == "3":
            system.create_agreement()
        elif choice == "4":
            system.record_payment()
        elif choice == "5":
            system.list_properties()
        elif choice == "6":
            system.list_tenants()
        elif choice == "7":
            system.list_agreements()
        elif choice == "0":
            print("👋 Exiting system...")
            break
        else:
            print("❌ Invalid choice, try again.")

    print("Goodbye!")

    # Save data to JSON file
    with open("properties.json", "w") as f:
        json.dump([p.to_dict() for p in system.properties], f)

    with open("tenants.json", "w") as f:
        json.dump([t.to_dict() for t in system.tenants], f)

    with open("agreements.json", "w") as f:
        json.dump([a.to_dict() for a in system.agreements], f)