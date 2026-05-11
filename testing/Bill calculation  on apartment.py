while True:
    # Ask for total rent amount
    total_rent = float(input("Enter the total rent amount: "))

    # Ask for number of people
    num_people = int(input("Enter the number of people: "))

    # Ask for utility bill (optional)
    utility_bill = float(input("Enter total utility bill (e.g., electricity/water): "))

    # Choose split method
    print("\nChoose split method:")
    print("1. Equal split")
    print("2. Weighted split (percentages)")
    print("3. Custom split (room size + facilities + usage)")
    print("4. Exit")
    choice = int(input("Enter choice (1/2/3/4): "))

    shares = []

    if choice == 1:
        # Equal split
        share = total_rent / num_people
        shares = [round(share, 2)] * num_people

    elif choice == 2:
        # Weighted split (percentages)
        print("\nEnter percentage for each person (must total 100):")
        percentages = []
        for i in range(num_people):
            p = float(input(f"Person {i+1} percentage: "))
            percentages.append(p)
        if sum(percentages) != 100:
            print("Error: Percentages must total 100!")
        else:
            shares = [round(total_rent * (p/100), 2) for p in percentages]

    elif choice == 3:
        # Custom splits bills 
        print("\nEnter room size (sq ft) for each person:")
        room_sizes = [float(input(f"Person {i+1} room size: ")) for i in range(num_people)]

        print("\nEnter facility surcharge (e.g., Balcony=50, AC=100) for each person:")
        facilities = [float(input(f"Person {i+1} facility surcharge: ")) for i in range(num_people)]

        print("\nEnter usage data (e.g., electricity kWh) for each person:")
        usage_data = [float(input(f"Person {i+1} usage: ")) for i in range(num_people)]

        total_size = sum(room_sizes)
        base_shares = [total_rent * (size / total_size) for size in room_sizes]

        facility_adjusted = [base + fac for base, fac in zip(base_shares, facilities)]

        total_usage = sum(usage_data)
        utility_shares = [utility_bill * (u / total_usage) for u in usage_data]

        shares = [round(base + util, 2) for base, util in zip(facility_adjusted, utility_shares)]

    elif choice == 4:
        print("Session ended.")
        break

    else:
        print("Invalid choice, try again.")

    # Display results if shares were calculated
    if shares:
        print("\n--- Rent Split Results ---")
        for i, s in enumerate(shares, start=1):
            print(f"Person {i} pays: RM{s}")
    print("\n")  # Add spacing before looping back

