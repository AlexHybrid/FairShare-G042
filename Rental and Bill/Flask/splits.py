
import cgi, cgitb
from cgi import escape

cgitb.enable()

form = cgi.FieldStorage()

# --- Rent split functions ---
def equal_split(total_rent, num_people):
    if num_people <= 0:
        return []
    share = total_rent / num_people
    return [round(share, 2)] * num_people

def weighted_split(total_rent, num_people, percentages):
    if not percentages or len(percentages) != num_people:
        raise ValueError("Percentages must match number of people")
    if round(sum(percentages), 2) == 100:
        return [round(total_rent * (p/100), 2) for p in percentages]
    else:
        raise ValueError("Percentages must total 100")

def custom_split(total_rent, utility_bill, room_sizes, facilities, usage_data):
    if not room_sizes or sum(room_sizes) == 0:
        raise ValueError("Room sizes must be provided")
    total_size = sum(room_sizes)
    base_shares = [total_rent * (size / total_size) for size in room_sizes]
    facility_adjusted = [base + fac for base, fac in zip(base_shares, facilities)]
    total_usage = sum(usage_data)
    utility_shares = [utility_bill * (u / total_usage) for u in usage_data] if total_usage > 0 else [0] * len(usage_data)
    return [round(base + util, 2) for base, util in zip(facility_adjusted, utility_shares)]

# --- Read form inputs safely ---
def safe_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default

def safe_int(val, default=1):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

# --- Handle form inputs ---
total_rent = safe_float(form.getvalue("total_rent"))
num_people = safe_int(form.getvalue("num_people"))
names = form.getlist("names") or [f"Person {i+1}" for i in range(num_people)]
utility_bill = safe_float(form.getvalue("utility_bill"))
method = form.getvalue("method") or "equal"

shares = []
error_message = None
try:
    if method == "equal":
        shares = equal_split(total_rent, num_people)
    elif method == "weighted":
        percentages = [safe_float(p) for p in form.getlist("percentages")]
        shares = weighted_split(total_rent, num_people, percentages)
    elif method == "custom":
        room_sizes = [safe_float(r) for r in form.getlist("room_sizes")]
        facilities = [safe_float(f) for f in form.getlist("facilities")]
        usage_data = [safe_float(u) for u in form.getlist("usage_data")]
        shares = custom_split(total_rent, utility_bill, room_sizes, facilities, usage_data)
except Exception as e:
    error_message = str(e)

# --- Output HTML ---
print("Content-Type: text/html\r\n\r\n")
print("<html><head><title>Results</title></head><body>")
print("<h2>Rent Split Results</h2>")
if error_message:
    print(f"<p style='color:red;'>Error: {escape(error_message)}</p>")
elif shares:
    for name, share in zip(names, shares):
        print(f"<p>{escape(name.strip())} pays: RM{escape(str(share))}</p>")
    print(f"<p>Total Rent: RM{escape(str(total_rent))}</p>")
    print(f"<p>Utility Bill: RM{escape(str(utility_bill))}</p>")
else:
    print("<p>No results calculated.</p>")
print("</body></html>") 