# 🏠 Rental System (Clients instead of Tenants)

class Property:
    def __init__(self, property_id, address, size, facilities, rent_price):
        self.property_id = property_id
        self.address = address
        self.size = size
        self.facilities = facilities
        self.rent_price = rent_price

    def __str__(self):
        return f"{self.property_id}: {self.address}, {self.size} sqft, Rent: RM{self.rent_price}"


class Client:
    def __init__(self, client_id, name, email, phone, occupation):
        self.client_id = client_id
        self.name = name
        self.email = email
        self.phone = phone
        self.occupation = occupation

    def __str__(self):
        return f"{self.client_id}: {self.name}, {self.occupation}, Email: {self.email}, Phone: {self.phone}"


class RentalAgreement:
    def __init__(self, agreement_id, client, property, start_date, end_date, monthly_rent):
        self.agreement_id = agreement_id
        self.client = client
        self.property = property
        self.start_date = start_date
        self.end_date = end_date
        self.monthly_rent = monthly_rent

    def __str__(self):
        return f"Agreement {self.agreement_id}: {self.client.name} renting {self.property.address} at RM{self.monthly_rent}/month"


class Payment:
    def __init__(self, payment_id, agreement, amount, date, status="Pending"):
        self.payment_id = payment_id
        self.agreement = agreement
        self.amount = amount
        self.date = date
        self.status = status

    def mark_paid(self):
        self.status = "Paid"


class RentalSystem:
    def __init__(self):
        self.properties = {}
        self.clients = {}
        self.agreements = {}
        self.payments = {}

    # Property Management
    def add_property(self, property_id, address, size, facilities, rent_price):
        self.properties[property_id] = Property(property_id, address, size, facilities, rent_price)

    def list_properties(self):
        for prop in self.properties.values():
            print(prop)

    # Client Management
    def add_client(self, client_id, name, email, phone, occupation):
        self.clients[client_id] = Client(client_id, name, email, phone, occupation)

    def list_clients(self):
        for client in self.clients.values():
            print(client)

    # Rental Agreements
    def create_agreement(self, agreement_id, client_id, property_id, start_date, end_date, monthly_rent):
        client = self.clients.get(client_id)
        property = self.properties.get(property_id)
        if client and property:
            self.agreements[agreement_id] = RentalAgreement(agreement_id, client, property, start_date, end_date, monthly_rent)

    def list_agreements(self):
        for agreement in self.agreements.values():
            print(agreement)

    # Payments
    def record_payment(self, payment_id, agreement_id, amount, date):
        agreement = self.agreements.get(agreement_id)
        if agreement:
            self.payments[payment_id] = Payment(payment_id, agreement, amount, date)

    def list_payments(self):
        for payment in self.payments.values():
            print(f"{payment.payment_id}: RM{payment.amount} for {payment.agreement.client.name}, Status: {payment.status}")


# Example Usage
if __name__ == "__main__":
    system = RentalSystem()

    # Add property
    system.add_property("P1", "Cyberjaya Apartment", 850, ["WiFi", "Parking"], 1200)

    # Add client (instead of tenant)
    system.add_client("C1", "Ali", "ali@example.com", "0123456789", "Software Engineer")

    # Create rental agreement
    system.create_agreement("A1", "C1", "P1", "2026-06-01", "2027-06-01", 1200)

    # Record payment
    system.record_payment("PAY1", "A1", 1200, "2026-06-01")

    # Display data
    system.list_properties()
    system.list_clients()
    system.list_agreements()
    system.list_payments()
