def get_float(prompt, allow_empty=False):
    while True:
        value = input(prompt)
        if allow_empty and value.strip() == "":
            return 0.0
        try:
            return float(value)
        except ValueError:
            print("Error: Please enter a valid number.")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Please enter a valid integer.")

def equal_split(total_rent, num_people):
    share = total_rent / num_people
    return [round(share, 2)] * num_people

def weighted_split(total_rent, num_people):
    while True:
        print("\nEnter percentage for each person (must total 100):")
        percentages = [get_float(f"Person {i+1} percentage: ") for i in range(num_people)]
        if round(sum(percentages), 2) == 100:
            return [round(total_rent * (p/100), 2) for p in percentages]
        print("Error: Percentages must total 100! Try again.")

def custom_split(total_rent, utility_bill, num_people):
    print("\nEnter room size (sq ft) for each person:")
    room_sizes = [get_float(f"Person {i+1} room size: ") for i in range(num_people)]

    print("\nEnter facility surcharge (e.g., Balcony=50, AC=100) for each person:")
    facilities = [get_float(f"Person {i+1} facility surcharge: ") for i in range(num_people)]

    print("\nEnter usage data (e.g., electricity kWh) for each person:")
    usage_data = [get_float(f"Person {i+1} usage: ") for i in range(num_people)]

    total_size = sum(room_sizes)
    base_shares = [total_rent * (size / total_size) for size in room_sizes]

    facility_adjusted = [base + fac for base, fac in zip(base_shares, facilities)]

    total_usage = sum(usage_data)
    utility_shares = [utility_bill * (u / total_usage) for u in usage_data] if total_usage > 0 else [0] * num_people

    return [round(base + util, 2) for base, util in zip(facility_adjusted, utility_shares)]

def display_results(names, shares, total_rent, utility_bill):
    print("\n--- Rent Split Results ---")
    for name, share in zip(names, shares):
        print(f"{name} pays: RM{share}")
    print("--------------------------")
    print(f"Total Rent: RM{total_rent}")
    print(f"Utility Bill: RM{utility_bill}")
    print("\n")

# Main session loop
while True:
    total_rent = get_float("Enter the total rent amount: ")
    num_people = get_int("Enter the number of people: ")
    names = [input(f"Enter name for person {i+1}: ") for i in range(num_people)]
    utility_bill = get_float("Enter total utility bill (or press Enter to skip): ", allow_empty=True)

    # Split method loop
    while True:
        print("\nChoose split method:")
        print("1. Equal split")
        print("2. Weighted split (percentages)")
        print("3. Custom split (room size + facilities + usage)")
        print("4. Exit to main menu")
        choice = get_int("Enter choice (1/2/3/4): ")

        shares = []

        if choice == 1:
            shares = equal_split(total_rent, num_people)
        elif choice == 2:
            shares = weighted_split(total_rent, num_people)
        elif choice == 3:
            shares = custom_split(total_rent, utility_bill, num_people)
        elif choice == 4:
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid choice, try again.")

        if shares:
            display_results(names, shares, total_rent, utility_bill)
