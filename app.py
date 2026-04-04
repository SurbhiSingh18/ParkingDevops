from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

slots = [f"Slot {i}" for i in range(1, 21)]

# Structure:
# {
#   "2026-04-03": {
#       "Slot 1": {details}
#   }
# }
booked_slots = {}

# ---------------- HOME ----------------
@app.route('/')
def home():
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

# ---------------- BOOK ----------------
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    college_id = request.form['college_id']
    password = request.form['password']
    vehicle = request.form['vehicle']
    slot = request.form['slot']
    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    if date not in booked_slots:
        booked_slots[date] = {}

    if slot in booked_slots[date]:
        return redirect('/?msg=already')

    booked_slots[date][slot] = {
        "name": name,
        "college_id": college_id,
        "password": password,
        "vehicle": vehicle,
        "start_time": start_time,
        "end_time": end_time
    }

    return redirect('/?date=' + date + '&msg=success')

# ---------------- CANCEL ----------------
@app.route('/cancel', methods=['POST'])
def cancel():
    slot = request.form['slot']
    date = request.form['date']
    entered_id = request.form['college_id']
    entered_password = request.form['password']

    if date in booked_slots and slot in booked_slots[date]:
        booking = booked_slots[date][slot]

        if booking["college_id"] == entered_id and booking["password"] == entered_password:
            del booked_slots[date][slot]
            return redirect('/?msg=cancelled')
        else:
            return redirect('/?msg=invalid')

    return redirect('/')

# ---------------- BOOKINGS DASHBOARD ----------------
@app.route('/bookings')
def bookings():
    sorted_dates = sorted(booked_slots.keys())

    return render_template(
        'bookings.html',
        booked_slots=booked_slots,
        dates=sorted_dates,
        slots=slots
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)