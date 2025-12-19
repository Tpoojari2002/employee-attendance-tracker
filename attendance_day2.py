from attendance_day1 import cursor, conn
from datetime import datetime
import logging

def update_attendance_status():
    today = datetime.now().date()

    cursor.execute(
        "SELECT emp_id, work_hours FROM attendance WHERE date=%s",
        (today,)
    )

    for emp_id, work_hours in cursor.fetchall():
        if work_hours is None:
            continue

        if work_hours < 8:
            status = "Underworked"
            logging.warning(f"Employee {emp_id} underworked ({work_hours:.2f} hrs)")
        else:
            status = "Present"

        cursor.execute(
            "UPDATE attendance SET status=%s WHERE emp_id=%s AND date=%s",
            (status, emp_id, today)
        )

    conn.commit()


def daily_attendance_report():
    today = datetime.now().date()

    cursor.execute("""
        SELECT e.emp_name,
               a.login_time,
               a.logout_time,
               ROUND(a.work_hours,2),
               a.status
        FROM attendance a
        JOIN employee e ON a.emp_id = e.emp_id
        WHERE a.date = %s
    """, (today,))

    records = cursor.fetchall()

    print("\n📋 DAILY ATTENDANCE REPORT")
    print("-" * 60)
    print(f"{'Name':15}{'Login':20}{'Logout':20}{'Hours':8}{'Status'}")
    print("-" * 60)

    for r in records:
        name = r[0]
        login = r[1] if r[1] else "N/A"
        logout = r[2] if r[2] else "N/A"
        hours = f"{r[3]:.2f}" if r[3] is not None else "N/A"
        status = r[4] if r[4] else "Pending"

        print(f"{name:15}{str(login):20}{str(logout):20}{hours:8}{status}")


update_attendance_status()
daily_attendance_report()
