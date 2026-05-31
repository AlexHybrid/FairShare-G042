# 🏠 Rental Management System with Menu

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

    def add_property(self):
        pid = len(self.properties) + 1
        address = input("Enter property address: ")
        rent = float(input("Enter monthly rent: RM"))
        p = Property(pid, address, rent)
        self.properties.append(p)
        print("✅ Property added!")

    def register_tenant(self):
        tid = len(self.tenants) + 1
        name = input("Enter tenant name: ")
        contact = input("Enter tenant contact: ")
        t = Tenant(tid, name, contact)
        self.tenants.append(t)
        print("✅ Tenant registered!")

    def create_agreement(self):
        if not self.properties or not self.tenants:
            print("⚠️ Add property and tenant first!")
            return
        self.list_properties()
        pid = int(input("Choose property ID: "))
        self.list_tenants()
        tid = int(input("Choose tenant ID: "))
        start = input("Enter start date (YYYY-MM-DD): ")
        end = input("Enter end date (YYYY-MM-DD): ")
        deposit = float(input("Enter deposit amount: RM"))
        agreement = RentalAgreement(self.properties[pid-1], self.tenants[tid-1], start, end, deposit)
        self.agreements.append(agreement)
        self.properties[pid-1].assign_tenant(self.tenants[tid-1])
        print("✅ Agreement created!")

    def list_properties(self):
        for p in self.properties:
            print(p)

    def list_tenants(self):
        for t in self.tenants:
            print(t)

    def list_agreements(self):
        for a in self.agreements:
            print(a)


# 🚀 Menu-driven program
if __name__ == "__main__":
    system = RentalSystem()

    while True:
        print("\n--- Rental System Menu ---")
        print("1. Add Property")
        print("2. Register Tenant")
        print("3. Create Agreement")
        print("4. List Properties")
        print("5. List Tenants")
        print("6. List Agreements")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            system.add_property()
        elif choice == "2":
            system.register_tenant()
        elif choice == "3":
            system.create_agreement()
        elif choice == "4":
            system.list_properties()
        elif choice == "5":
            system.list_tenants()
        elif choice == "6":
            system.list_agreements()
        elif choice == "0":
            print("👋 Exiting system...")
            break
        else:
            print("❌ Invalid choice, try again.")
