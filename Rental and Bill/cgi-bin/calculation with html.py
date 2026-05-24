#!/usr/bin/env python3
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()

# --- Rent split functions ---
def equal_split(total_rent, num_people):
    share = total_rent / num_people
    return [round(share, 2)] * num_people

def weighted_split(total_rent, num_people, percentages):
    if round(sum(percentages), 2) == 100:
        return [round(total_rent * (p/100), 2) for p in percentages]
    else:
        raise ValueError("Percentages must total 100")

def custom_split(total_rent, utility_bill, room_sizes, facilities, usage_data):
    total_size = sum(room_sizes)
    base_shares = [total_rent * (size / total_size) for size in room_sizes]
    facility_adjusted = [base + fac for base, fac in zip(base_shares, facilities)]
    total_usage = sum(usage_data)
    utility_shares = [utility_bill * (u / total_usage) for u in usage_data] if total_usage > 0 else [0] * len(usage_data)
    return [round(base + util, 2) for base, util in zip(facility_adjusted, utility_shares)]

# --- Read form inputs ---
total_rent = float(form.getvalue("total_rent", 0))
num_people = int(form.getvalue("num_people", 1))
names = form.getlist("names")
utility_bill = float(form.getvalue("utility_bill", 0))
method = form.getvalue("method", "equal")

shares = []
try:
    if method == "equal":
        shares = equal_split(total_rent, num_people)
    elif method == "weighted":
        percentages = [float(p) for p in form.getlist("percentages")]
        shares = weighted_split(total_rent, num_people, percentages)
    elif method == "custom":
        room_sizes = [float(r) for r in form.getlist("room_sizes")]
        facilities = [float(f) for f in form.getlist("facilities")]
        usage_data = [float(u) for u in form.getlist("usage_data")]
        shares = custom_split(total_rent, utility_bill, room_sizes, facilities, usage_data)
except Exception as e:
    shares = [f"Error: {str(e)}"]

# --- Output HTML ---
print("Content-Type: text/html\n")
print("<html><head><title>Results</title></head><body>")
print("<h2>Rent Split Results</h2>")
if shares and isinstance(shares[0], str):
    print(f"<p>{shares[0]}</p>")
else:
    for name, share in zip(names, shares):
        print(f"<p>{name} pays: RM{share}</p>")
print(f"<p>Total Rent: RM{total_rent}</p>")
print(f"<p>Utility Bill: RM{utility_bill}</p>")
print("</body></html>")
