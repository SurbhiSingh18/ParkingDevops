import sqlite3
import os

DATABASE_NAME = 'parking.db'

def init_database():
    """Initialize the SQLite database with required tables"""
    if os.path.exists(DATABASE_NAME):
        print(f"Database {DATABASE_NAME} already exists")
        return
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            slot TEXT NOT NULL,
            name TEXT NOT NULL,
            college_id TEXT NOT NULL,
            password TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, slot)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database {DATABASE_NAME} created successfully")

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def get_bookings_by_date(date):
    """Get all bookings for a specific date"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE date = ?', (date,))
    bookings = cursor.fetchall()
    conn.close()
    
    # Convert to the format expected by the template
    result = {}
    for booking in bookings:
        slot = booking['slot']
        result[slot] = {
            'name': booking['name'],
            'college_id': booking['college_id'],
            'password': booking['password'],
            'vehicle': booking['vehicle'],
            'start_time': booking['start_time'],
            'end_time': booking['end_time']
        }
    return result

def create_booking(date, slot, name, college_id, password, vehicle, start_time, end_time):
    """Create a new booking"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO bookings (date, slot, name, college_id, password, vehicle, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, slot, name, college_id, password, vehicle, start_time, end_time))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Slot already booked for this date
    finally:
        conn.close()

def cancel_booking(date, slot, college_id, password):
    """Cancel a booking"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM bookings 
        WHERE date = ? AND slot = ? AND college_id = ? AND password = ?
    ''', (date, slot, college_id, password))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0

def get_all_booked_dates():
    """Get all dates that have bookings"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT date FROM bookings ORDER BY date')
    dates = [row['date'] for row in cursor.fetchall()]
    conn.close()
    return dates

if __name__ == '__main__':
    init_database()
