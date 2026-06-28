# Enhanced Python Bill Splitter with Loop

while True:
    # Ask for total bill amount
    total_bill = float(input("Enter the total bill amount: "))

    # Ask for number of people
    num_people = int(input("Enter the number of people: "))

    # Choose split method
    print("\nChoose split method:")
    print("1. Equal split")
    print("2. Weighted split (percentages)")
    print("3. Custom split (manual amounts)")
    print("4. Exit")
    choice = int(input("Enter choice (1/2/3/4): "))

    shares = []

    if choice == 1:
        # Equal split
        share = total_bill / num_people
        shares = [round(share, 2)] * num_people

    elif choice == 2:
        # Weighted split 
        print("\nEnter percentage for each person (must total 100):")
        percentages = []
        for i in range(num_people):
            p = float(input(f"Person {i+1} percentage: "))
            percentages.append(p)
        if sum(percentages) != 100:
            print("Error: Percentages must total 100!")
        else:
            shares = [round(total_bill * (p/100), 2) for p in percentages]

    elif choice == 3:
        # Custom split
        print("\nEnter amount for each person (must total bill):")
        amounts = []
        for i in range(num_people):
            a = float(input(f"Person {i+1} amount: "))
            amounts.append(a)
        if sum(amounts) != total_bill:
            print("Error: Amounts must total bill!")
        else:
            shares = [round(a, 2) for a in amounts]

    elif choice == 4:
        print("Exiting program...")
        break

    else:
        print("Invalid choice, try again.")

    # Display results if shares were calculated
    if shares:
        print("\n--- Bill Split Results ---")
        for i, s in enumerate(shares, start=1):
            print(f"Person {i} pays: RM{s}")
    print("\n")  # Add spacing before looping back


