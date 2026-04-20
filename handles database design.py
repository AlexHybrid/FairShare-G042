# Simple Python program: Bill Splitter

# Ask for total bill amount
total_bill = float(input("Enter the total bill amount: "))

# Ask for number of people
num_people = int(input("Enter the number of people: "))

# Calculate each person's share
share = total_bill / num_people

# Display result
print("Each person should pay: RM", round(share, 2))
