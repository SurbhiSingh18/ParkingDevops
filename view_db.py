import sqlite3
from database import get_db_connection

def view_database():
    """View all data in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("=== PARKING BOOKING DATABASE ===\n")
    
    # View all bookings
    cursor.execute('SELECT * FROM bookings ORDER BY date, slot')
    bookings = cursor.fetchall()
    
    if not bookings:
        print("No bookings found in database.")
    else:
        print(f"Total Bookings: {len(bookings)}\n")
        print("ID | Date      | Slot   | Name         | College ID | Vehicle | Start | End | Created At")
        print("-" * 100)
        
        for booking in bookings:
            print(f"{booking['id']:3} | {booking['date']:10} | {booking['slot']:6} | {booking['name']:12} | {booking['college_id']:10} | {booking['vehicle']:7} | {booking['start_time']:5} | {booking['end_time']:4} | {booking['created_at']}")
    
    conn.close()

if __name__ == '__main__':
    view_database()
