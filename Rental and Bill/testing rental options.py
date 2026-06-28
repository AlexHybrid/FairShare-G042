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
      ╔═══════════════════════════════╗
      ║   ░█▀█░█▀█░█▄█░█▀█░█░█░█▀█    ║
      ║        RENTAL BLOSSOMS        ║
      ║   Homes • Tenants • Rent      ║
      ╚═══════════════════════════════╝
    """ + "\033[0m")


# ------------------ Classes ------------------
class Property:
    def __init__(self, property_id, address, rent_price, tenant=None):
        self.property_id = property_id
        self.address = address
        self.rent_price = rent_price
        self.tenant = tenant

    def assign_tenant(self, tenant):
        self.tenant = tenant

    def to_dict(self):
        return {
            "property_id": self.property_id,
            "address": self.address,
            "rent_price": self.rent_price,
            "tenant": self.tenant.tenant_id if self.tenant else None
        }

    def __str__(self):
        return f"{GREEN}Property {self.property_id}:{RESET} {self.address} | Rent: RM{self.rent_price} | Tenant: {self.tenant.name if self.tenant else 'None'}"


class Tenant:
    def __init__(self, tenant_id, name, contact):
        self.tenant_id = tenant_id
        self.name = name
        self.contact = contact

    def to_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "name": self.name,
            "contact": self.contact
        }

    def __str__(self):
        return f"{BLUE}Tenant {self.tenant_id}:{RESET} {self.name} ({self.contact})"


class RentalAgreement:
    def __init__(self, property, tenant, start_date, end_date, deposit, payments=None):
        self.property = property
        self.tenant = tenant
        self.start_date = start_date
        self.end_date = end_date
        self.deposit = deposit
        self.payments = payments if payments else []

    def add_payment(self, amount, date):
        self.payments.append({"amount": amount, "date": date})

    def to_dict(self):
        return {
            "property_id": self.property.property_id,
            "tenant_id": self.tenant.tenant_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "deposit": self.deposit,
            "payments": self.payments
        }

    def __str__(self):
        return f"{MAGENTA}Agreement:{RESET} {self.tenant.name} renting {self.property.address} from {self.start_date} to {self.end_date}"


# ------------------ System ------------------
class RentalSystem:
    def __init__(self, filename="rental_data.json"):
        self.properties = []
        self.tenants = []
        self.agreements = []
        self.filename = filename
        self.load_data()

    # Save data to JSON
    def save_data(self):
        data = {
            "properties": [p.to_dict() for p in self.properties],
            "tenants": [t.to_dict() for t in self.tenants],
            "agreements": [a.to_dict() for a in self.agreements]
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    # Load data from JSON
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)

            # Rebuild tenants
            self.tenants = [Tenant(**t) for t in data.get("tenants", [])]

            # Rebuild properties
            self.properties = []
            for p in data.get("properties", []):
                tenant = next((t for t in self.tenants if t.tenant_id == p["tenant"]), None)
                self.properties.append(Property(p["property_id"], p["address"], p["rent_price"], tenant))

            # Rebuild agreements
            self.agreements = []
            for a in data.get("agreements", []):
                property = next((p for p in self.properties if p.property_id == a["property_id"]), None)
                tenant = next((t for t in self.tenants if t.tenant_id == a["tenant_id"]), None)
                self.agreements.append(RentalAgreement(property, tenant, a["start_date"], a["end_date"], a["deposit"], a["payments"]))

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
        self.save_data()
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
        self.save_data()
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
        self.save_data()
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
        self.save_data()
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