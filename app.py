from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

slots = [f"Slot {i}" for i in range(1, 21)]
booked_slots = {}

@app.route('/')
def home():
    today = datetime.today().date()
    max_date = today + timedelta(days=7)
    return render_template('index.html', 
                           slots=slots, 
                           booked_slots=booked_slots,
                           min_date=today,
                           max_date=max_date)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    vehicle = request.form['vehicle']
    slot = request.form['slot']
    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    if slot in booked_slots:
        return redirect('/?msg=already')

    booked_slots[slot] = {
        "name": name,
        "vehicle": vehicle,
        "date": date,
        "start_time": start_time,
        "end_time": end_time
    }

    return redirect('/bookings')

@app.route('/cancel/<slot>')
def cancel(slot):
    if slot in booked_slots:
        del booked_slots[slot]
    return redirect('/?msg=cancelled')

@app.route('/bookings')
def bookings():
    return render_template('bookings.html', booked_slots=booked_slots)

if __name__ == '__main__':
    app.run(debug=True)