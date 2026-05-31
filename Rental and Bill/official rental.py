import os
import json

# Utility function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ANSI color codes
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"

def banner():
    print("\033[96m" + """
      🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸
      🌸     RENTAL BLOSSOMS           🌸
      🌸  Homes • Tenants • Rent       🌸
      🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸
    """ + "\033[0m")



class Property:
    def __init__(self, property_id, address, rent_price):
        self.property_id = property_id
        self.address = address
        self.rent_price = rent_price
        self.tenant = None

    def assign_tenant(self, tenant):
        self.tenant = tenant

    def __str__(self):
        return f"{GREEN}Property {self.property_id}:{RESET} {self.address} | Rent: RM{self.rent_price} | Tenant: {self.tenant.name if self.tenant else 'None'}"


class Tenant:
    def __init__(self, tenant_id, name, contact):
        self.tenant_id = tenant_id
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"{BLUE}Tenant {self.tenant_id}:{RESET} {self.name} ({self.contact})"


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
        return f"{MAGENTA}Agreement:{RESET} {self.tenant.name} renting {self.property.address} from {self.start_date} to {self.end_date}"


class RentalSystem:
    def __init__(self):
        self.properties = []
        self.tenants = []
        self.agreements = []

    # 📌 Property Management
    def add_property(self):
        clear_screen()
        banner()
        pid = len(self.properties) + 1
        address = input(CYAN + "Enter property address: " + RESET)
        try:
            rent = float(input(CYAN + "Enter monthly rent: RM" + RESET))
        except ValueError:
            print(RED + "❌ Rent must be a number!" + RESET)
            return
        p = Property(pid, address, rent)
        self.properties.append(p)
        print(GREEN + "✅ Property added!" + RESET)

    # 📌 Tenant Management
    def register_tenant(self):
        clear_screen()
        banner()
        tid = len(self.tenants) + 1
        name = input(CYAN + "Enter tenant name: " + RESET)
        contact = input(CYAN + "Enter tenant contact: " + RESET)
        t = Tenant(tid, name, contact)
        self.tenants.append(t)
        print(GREEN + "✅ Tenant registered!" + RESET)

    # 📌 Agreement Creation
    def create_agreement(self):
        clear_screen()
        banner()
        if not self.properties or not self.tenants:
            print(YELLOW + "⚠️ Add property and tenant first!" + RESET)
            return

        self.list_properties()
        try:
            pid = int(input(CYAN + "Choose property ID: " + RESET))
            property = next((p for p in self.properties if p.property_id == pid), None)
            if not property:
                print(RED + "❌ Invalid property ID!" + RESET)
                return
        except ValueError:
            print(RED + "❌ Please enter a valid number!" + RESET)
            return

        self.list_tenants()
        try:
            tid = int(input(CYAN + "Choose tenant ID: " + RESET))
            tenant = next((t for t in self.tenants if t.tenant_id == tid), None)
            if not tenant:
                print(RED + "❌ Invalid tenant ID!" + RESET)
                return
        except ValueError:
            print(RED + "❌ Please enter a valid number!" + RESET)
            return

        start = input(CYAN + "Enter start date (YYYY-MM-DD): " + RESET)
        end = input(CYAN + "Enter end date (YYYY-MM-DD): " + RESET)
        try:
            deposit = float(input(CYAN + "Enter deposit amount: RM" + RESET))
        except ValueError:
            print(RED + "❌ Deposit must be a number!" + RESET)
            return

        agreement = RentalAgreement(property, tenant, start, end, deposit)
        self.agreements.append(agreement)
        property.assign_tenant(tenant)
        print(GREEN + "✅ Agreement created!" + RESET)

    # 📌 Payment Tracking
    def record_payment(self):
        clear_screen()
        banner()
        if not self.agreements:
            print(YELLOW + "⚠️ No agreements found!" + RESET)
            return

        self.list_agreements()
        try:
            aid = int(input(CYAN + "Choose agreement number (1..N): " + RESET))
            agreement = self.agreements[aid-1]
        except (ValueError, IndexError):
            print(RED + "❌ Invalid agreement selection!" + RESET)
            return

        try:
            amount = float(input(CYAN + "Enter payment amount: RM" + RESET))
        except ValueError:
            print(RED + "❌ Payment must be a number!" + RESET)
            return

        date = input(CYAN + "Enter payment date (YYYY-MM-DD): " + RESET)
        agreement.add_payment(amount, date)
        print(GREEN + "✅ Payment recorded!" + RESET)

    # 📌 Listing
    def list_properties(self):
        print(YELLOW + "\n--- Properties ---" + RESET)
        if not self.properties:
            print(RED + "⚠️ No properties available." + RESET)
        else:
            for p in self.properties:
                print(p)

    def list_tenants(self):
        print(YELLOW + "\n--- Tenants ---" + RESET)
        if not self.tenants:
            print(RED + "⚠️ No tenants registered." + RESET)
        else:
            for t in self.tenants:
                print(t)

    def list_agreements(self):
        print(YELLOW + "\n--- Agreements ---" + RESET)
        if not self.agreements:
            print(RED + "⚠️ No agreements created." + RESET)
        else:
            for i, a in enumerate(self.agreements, start=1):
                print(f"{i}. {a}")
                if a.payments:
                    print("   Payments:")
                    for pay in a.payments:
                        print(f"     - RM{pay['amount']} on {pay['date']}")


# 🚀 Menu-driven program
if __name__ == "__main__":
    system = RentalSystem()

    while True:
        clear_screen()
        banner()
        print(YELLOW + "--- Main Menu ---" + RESET)
        print(CYAN + "1. Add Property" + RESET)
        print(CYAN + "2. Register Tenant" + RESET)
        print(CYAN + "3. Create Agreement" + RESET)
        print(CYAN + "4. Record Payment" + RESET)
        print(CYAN + "5. List Properties" + RESET)
        print(CYAN + "6. List Tenants" + RESET)
        print(CYAN + "7. List Agreements" + RESET)
        print(RED + "0. Exit" + RESET)

        choice = input(MAGENTA + "\nChoose an option: " + RESET)

        if choice == "1":
            system.add_property()
        elif choice == "2":
            system.register_tenant()
        elif choice == "3":
            system.create_agreement()
        elif choice == "4":
            system.record_payment()
        elif choice == "5":
            clear_screen(); banner(); system.list_properties(); input("\nPress Enter to return...")
        elif choice == "6":
            clear_screen(); banner(); system.list_tenants(); input("\nPress Enter to return...")
        elif choice == "7":
            clear_screen(); banner(); system.list_agreements(); input("\nPress Enter to return...")
        elif choice == "0":
            print(GREEN + "👋 Exiting system..." + RESET)
            break
        else:
            print(RED + "❌ Invalid choice! Please try again." + RESET)
            input("\nPress Enter to return to menu...") 