import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("HANA_SCHEMA")


def insert_seed_data(cursor):
    print("\n" + "=" * 60)
    print("STEP 2: INSERTING SEED DATA")
    print("=" * 60)

    departments = [
        (1, "Cardiology", 2),
        (2, "Orthopedics", 3),
        (3, "General Medicine", 1),
        (4, "Pediatrics", 2),
    ]
    cursor.executemany(
        f"INSERT INTO {SCHEMA}.DEPARTMENTS VALUES (?, ?, ?)", departments
    )
    print(f"Inserted {len(departments)} departments")

    doctors = [
        (1, "Dr. Rajesh Mehta", 1, "Cardiologist", 1000.00),
        (2, "Dr. Ananya Sharma", 1, "Interventional Cardiologist", 1500.00),
        (3, "Dr. Vikram Patel", 2, "Orthopedic Surgeon", 1200.00),
        (4, "Dr. Sneha Reddy", 2, "Sports Medicine Specialist", 800.00),
        (5, "Dr. Amit Verma", 3, "General Physician", 500.00),
        (6, "Dr. Priya Singh", 3, "Diabetologist", 700.00),
        (7, "Dr. Sunil Kapoor", 4, "Pediatrician", 600.00),
        (8, "Dr. Neha Gupta", 4, "Child Specialist", 900.00),
    ]
    cursor.executemany(
        f"INSERT INTO {SCHEMA}.DOCTORS VALUES (?, ?, ?, ?, ?)", doctors
    )
    print(f"Inserted {len(doctors)} doctors")

    patients = [
        (1, "Aarav Sharma", "Male", 32, "Delhi", "9876543210"),
        (2, "Priya Patel", "Female", 28, "Mumbai", "9876543211"),
        (3, "Rahul Kumar", "Male", 45, "Bangalore", "9876543212"),
        (4, "Sneha Gupta", "Female", 35, "Patna", "9876543213"),
        (5, "Vikram Singh", "Male", 50, "Kolkata", "9876543214"),
        (6, "Ananya Reddy", "Female", 27, "Chennai", "9876543215"),
        (7, "Amit Verma", "Male", 40, "Pune", "9876543216"),
        (8, "Neha Joshi", "Female", 55, "Delhi", "9876543217"),
        (9, "Rajesh Tiwari", "Male", 60, "Mumbai", "9876543218"),
        (10, "Pooja Mehta", "Female", 30, "Bangalore", "9876543219"),
        (11, "Deepak Nair", "Male", 38, "Patna", "9876543220"),
        (12, "Kavita Das", "Female", 42, "Kolkata", "9876543221"),
        (13, "Suresh Babu", "Male", 48, "Chennai", "9876543222"),
        (14, "Meera Iyer", "Female", 29, "Pune", "9876543223"),
        (15, "Arjun Khanna", "Male", 33, "Delhi", "9876543224"),
    ]
    cursor.executemany(
        f"INSERT INTO {SCHEMA}.PATIENTS VALUES (?, ?, ?, ?, ?, ?)", patients
    )
    print(f"Inserted {len(patients)} patients")

    appointments = [
        (1, 1, 1, "2026-06-01", "09:00:00", "Completed"),
        (2, 2, 2, "2026-06-01", "10:30:00", "Completed"),
        (3, 3, 3, "2026-06-02", "09:30:00", "Completed"),
        (4, 4, 5, "2026-06-02", "11:00:00", "Completed"),
        (5, 5, 7, "2026-06-03", "10:00:00", "Completed"),
        (6, 6, 4, "2026-06-03", "14:00:00", "Completed"),
        (7, 7, 6, "2026-06-04", "09:00:00", "Completed"),
        (8, 8, 8, "2026-06-05", "11:30:00", "Completed"),
        (9, 9, 1, "2026-06-05", "15:00:00", "Completed"),
        (10, 10, 2, "2026-06-06", "10:30:00", "Completed"),
        (11, 11, 3, "2026-06-07", "09:00:00", "Completed"),
        (12, 12, 5, "2026-06-08", "14:30:00", "Completed"),
        (13, 13, 7, "2026-06-03", "16:00:00", "Pending"),
        (14, 14, 4, "2026-06-06", "12:00:00", "Pending"),
        (15, 15, 6, "2026-06-08", "09:30:00", "Pending"),
        (16, 1, 8, "2026-06-10", "11:00:00", "Pending"),
        (17, 3, 1, "2026-06-02", "16:30:00", "Cancelled"),
        (18, 4, 3, "2026-06-04", "10:00:00", "Cancelled"),
        (19, 5, 5, "2026-06-07", "15:30:00", "Cancelled"),
        (20, 2, 2, "2026-06-10", "14:00:00", "Cancelled"),
    ]
    cursor.executemany(
        f"INSERT INTO {SCHEMA}.APPOINTMENTS VALUES (?, ?, ?, ?, ?, ?)", appointments
    )
    print(f"Inserted {len(appointments)} appointments")

    billing = [
        (1, 1, 1000.00, "Cash", "Paid"),
        (2, 2, 1550.00, "UPI", "Paid"),
        (3, 3, 1250.00, "Card", "Paid"),
        (4, 4, 600.00, "Cash", "Paid"),
        (5, 5, 700.00, "Insurance", "Paid"),
        (6, 6, 900.00, "UPI", "Paid"),
        (7, 7, 750.00, "Card", "Paid"),
        (8, 8, 950.00, "Cash", "Paid"),
        (9, 9, 1100.00, "Card", "Paid"),
        (10, 10, 1600.00, "UPI", "Refunded"),
        (11, 11, 1300.00, "Insurance", "Paid"),
        (12, 12, 550.00, "UPI", "Paid"),
        (13, 13, 650.00, "Cash", "Unpaid"),
        (14, 14, 900.00, "Card", "Unpaid"),
        (15, 15, 550.00, "UPI", "Unpaid"),
        (16, 20, 1550.00, "Card", "Refunded"),
    ]
    cursor.executemany(
        f"INSERT INTO {SCHEMA}.BILLING VALUES (?, ?, ?, ?, ?)", billing
    )
    print(f"Inserted {len(billing)} billing records")

    print("\nSeed data inserted successfully.")