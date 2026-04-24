from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
from database import init_database, get_bookings_by_date, create_booking, cancel_booking, get_all_booked_dates, get_db_connection

app = Flask(__name__)

slots = [f"Slot {i}" for i in range(1, 21)]

# Initialize database
init_database()

# ---------------- HOME ----------------
@app.route('/')
def home():
    today = datetime.today().date()
    max_date = today + timedelta(days=1)

    # Get selected date from URL or default to today
    selected_date = request.args.get("date")
    if not selected_date:
        selected_date = today.strftime('%Y-%m-%d')

    current_bookings = get_bookings_by_date(selected_date)

    return render_template(
        'index.html',
        slots=slots,
        booked_slots=current_bookings,
        min_date=today,
        max_date=max_date,
        selected_date=selected_date
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

    # Try to create booking in database
    success = create_booking(date, slot, name, college_id, password, vehicle, start_time, end_time)
    
    if not success:
        return redirect('/?msg=already')

    return redirect('/?date=' + date + '&msg=success')

# ---------------- CANCEL ----------------
@app.route('/cancel', methods=['POST'])
def cancel():
    slot = request.form['slot']
    date = request.form['date']
    entered_id = request.form['college_id']
    entered_password = request.form['password']

    # Try to cancel booking in database
    success = cancel_booking(date, slot, entered_id, entered_password)
    
    if success:
        return redirect('/?msg=cancelled')
    else:
        return redirect('/?msg=invalid')

    return redirect('/')

# ---------------- BOOKINGS DASHBOARD ----------------
@app.route('/bookings')
def bookings():
    sorted_dates = get_all_booked_dates()
    
    # Get all bookings data for the template
    all_bookings = {}
    for date in sorted_dates:
        all_bookings[date] = get_bookings_by_date(date)

    return render_template(
        'bookings.html',
        booked_slots=all_bookings,
        dates=sorted_dates,
        slots=slots
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)