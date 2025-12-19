import mysql.connector
from datetime import datetime, time
import logging

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Priacc@2025",
    database="attendance_system"
)

cursor = conn.cursor()

#Logging Setup

logging.basicConfig(
    filename="attendance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#Employee Login Function
def employee_login(emp_id):
    today = datetime.now().date()
    login_time = datetime.now()

    cursor.execute(
        "SELECT * FROM attendance WHERE emp_id=%s AND date=%s",
        (emp_id, today)
    )

    record = cursor.fetchone()

    if record:
        print(" Duplicate login not allowed")
        logging.warning(f"Duplicate login attempt by Employee {emp_id}")
    else:
        cursor.execute(
            "INSERT INTO attendance (emp_id, login_time, date) VALUES (%s, %s, %s)",
            (emp_id, login_time, today)
        )
        conn.commit()
        print("Login successful")
        logging.info(f"Employee {emp_id} logged in")

#Employee Logout Function
def employee_logout(emp_id):
    today = datetime.now().date()
    logout_time = datetime.now()

    cursor.execute(
        "SELECT login_time FROM attendance WHERE emp_id=%s AND date=%s AND logout_time IS NULL",
        (emp_id, today)
    )

    record = cursor.fetchone()

    if not record:
        print(" No active login found")
        return

    login_time = record[0]
    work_hours = (logout_time - login_time).total_seconds() / 3600

    cursor.execute(
        """UPDATE attendance
           SET logout_time=%s, work_hours=%s
           WHERE emp_id=%s AND date=%s""",
        (logout_time, work_hours, emp_id, today)
    )

    conn.commit()
    print(f" Logout successful | Work Hours: {round(work_hours,2)}")
    logging.info(f"Employee {emp_id} logged out")

#Missing Logout

def auto_logout():
    today = datetime.now().date()
    auto_logout_time = datetime.combine(today, time(19, 0))

    cursor.execute(
        "SELECT emp_id, login_time FROM attendance WHERE date=%s AND logout_time IS NULL",
        (today,)
    )

    records = cursor.fetchall()

    for emp_id, login_time in records:
        work_hours = (auto_logout_time - login_time).total_seconds() / 3600

        cursor.execute(
            """UPDATE attendance
               SET logout_time=%s, work_hours=%s
               WHERE emp_id=%s AND date=%s""",
            (auto_logout_time, work_hours, emp_id, today)
        )

        logging.info(f"Auto logout applied for Employee {emp_id}")

    conn.commit()


if __name__ == "__main__":
    while True:
        print("\n--- Employee Attendance System ---")
        print("1. Login")
        print("2. Logout")
        print("3. Auto Logout (7 PM)")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            emp_id = int(input("Enter Employee ID: "))
            employee_login(emp_id)

        elif choice == "2":
            emp_id = int(input("Enter Employee ID: "))
            employee_logout(emp_id)

        elif choice == "3":
            auto_logout()
            print("Auto logout completed")

        elif choice == "4":
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")

