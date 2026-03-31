from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

slots = [f"Slot {i}" for i in range(1, 21)]
booked_slots = {}  
# structure:
# {
#   "2026-04-03": {
#       "Slot 1": {details},
#       "Slot 2": {details}
#   }
# }

@app.route('/')
def home():
    from datetime import datetime, timedelta

    today = datetime.today().date()
    max_date = today + timedelta(days=7)

    selected_date = request.args.get("date")

    if selected_date and selected_date in booked_slots:
        current_bookings = booked_slots[selected_date]
    else:
        current_bookings = {}

    return render_template(
        'index.html',
        slots=slots,
        booked_slots=current_bookings,
        min_date=today,
        max_date=max_date
    )

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    vehicle = request.form['vehicle']
    slot = request.form['slot']
    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    date = request.form['date']

    if date not in booked_slots:
        booked_slots[date] = {}

    if slot in booked_slots[date]:
        return redirect('/?msg=already')

    booked_slots[date][slot] = {
        "name": name,
        "vehicle": vehicle,
        "start_time": start_time,
        "end_time": end_time
}

    return redirect('/?date=' + date + '&msg=success')

@app.route('/cancel/<date>/<slot>')
def cancel(date, slot):
    if date in booked_slots and slot in booked_slots[date]:
        del booked_slots[date][slot]

        if not booked_slots[date]:
            del booked_slots[date]

    return redirect('/?msg=cancelled')

@app.route('/bookings')
def bookings():
    all_bookings = []

    for date, slots_data in booked_slots.items():
        for slot, details in slots_data.items():
            slot_number = int(slot.split()[1])  # Slot 7 → 7

            all_bookings.append({
                "slot": slot,
                "slot_num": slot_number,
                "name": details["name"],
                "vehicle": details["vehicle"],
                "date": date,
                "start_time": details["start_time"],
                "end_time": details["end_time"]
            })

    # ✅ SORT BY DATE → SLOT NUMBER
    all_bookings.sort(key=lambda x: (x["date"], x["slot_num"]))

    return render_template('bookings.html', bookings=all_bookings)

if __name__ == '__main__':
    app.run(debug=True)