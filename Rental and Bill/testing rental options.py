# 🏠 Rental System Skeleton

class Property:
    def __init__(self, property_id, address, rent_price, size, facilities):
        self.property_id = property_id
        self.address = address
        self.rent_price = rent_price
        self.size = size
        self.facilities = facilities
        self.tenant = None

    def assign_tenant(self, tenant):
        self.tenant = tenant
        print(f"Tenant {tenant.name} assigned to property {self.address}")

    def remove_tenant(self):
        print(f"Tenant {self.tenant.name} removed from property {self.address}")
        self.tenant = None


class Tenant:
    def __init__(self, tenant_id, name, contact, id_number):
        self.tenant_id = tenant_id
        self.name = name
        self.contact = contact
        self.id_number = id_number


class RentalAgreement:
    def __init__(self, property, tenant, start_date, end_date, monthly_rent, deposit):
        self.property = property
        self.tenant = tenant
        self.start_date = start_date
        self.end_date = end_date
        self.monthly_rent = monthly_rent
        self.deposit = deposit
        self.payments = []

    def record_payment(self, amount, date):
        self.payments.append({"amount": amount, "date": date})
        print(f"Payment of {amount} recorded on {date}")

    def rental_history(self):
        return self.payments


class MaintenanceRequest:
    def __init__(self, tenant, description):
        self.tenant = tenant
        self.description = description
        self.status = "Pending"

    def update_status(self, new_status):
        self.status = new_status
        print(f"Request updated to {self.status}")


# Example usage
tenant1 = Tenant(1, "Ali", "0123456789", "IC123456")
property1 = Property(101, "Cyberjaya Apartment", 1200, "850 sqft", ["WiFi", "Parking"])

property1.assign_tenant(tenant1)

agreement1 = RentalAgreement(property1, tenant1, "2026-06-01", "2027-06-01", 1200, 2400)
agreement1.record_payment(1200, "2026-06-01")

request1 = MaintenanceRequest(tenant1, "Aircond not working")
request1.update_status("Completed")
