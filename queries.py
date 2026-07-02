import os
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("HANA_SCHEMA")


def run_query(cursor, title, sql):
    print(f"\n{'-' * 60}")
    print(f" {title}")
    print(f"{'-' * 60}")
    cursor.execute(sql)
    rows = cursor.fetchall()
    if not cursor.description:
        return
    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(v) for v in row))
    print(f"({len(rows)} rows)\n")

def run_business_queries(cursor):
    print("\n" + "=" * 60)
    print("STEP 4: RUNNING BUSINESS QUERIES")
    print("=" * 60)

    run_query(
        cursor,
        "Q1: All Completed OPD Appointments",
        f"""
            SELECT APPOINTMENT_ID, PATIENT_NAME, DEPARTMENT_NAME,
            APPOINTMENT_DATE, BILL_AMOUNT, PAYMENT_STATUS
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            WHERE APPOINTMENT_STATUS = 'Completed'
            ORDER BY APPOINTMENT_DATE
        """,
    )

    run_query(
        cursor,
        "Q2: Total OPD Revenue (Paid Bills Only)",
        f"""
            SELECT SUM(BILL_AMOUNT) AS TOTAL_REVENUE
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            WHERE PAYMENT_STATUS = 'Paid'
        """,
    )

    run_query(
        cursor,
        "Q3: Department-wise Revenue",
        f"""
            SELECT DEPARTMENT_NAME,
            SUM(BILL_AMOUNT) AS TOTAL_REVENUE
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            WHERE PAYMENT_STATUS = 'Paid'
            GROUP BY DEPARTMENT_NAME
            ORDER BY TOTAL_REVENUE DESC
        """,
    )

    run_query(
        cursor,
        "Q4: Doctor-wise Consultation Revenue",
        f"""
            SELECT DOCTOR_NAME, DEPARTMENT_NAME,
            COUNT(APPOINTMENT_ID) AS TOTAL_APPOINTMENTS,
            SUM(BILL_AMOUNT) AS TOTAL_REVENUE
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            WHERE PAYMENT_STATUS = 'Paid'
            GROUP BY DOCTOR_NAME, DEPARTMENT_NAME
            ORDER BY TOTAL_REVENUE DESC
        """,
    )

    run_query(
        cursor,
        "Q5: All Pending Appointments",
        f"""
            SELECT APPOINTMENT_ID, PATIENT_NAME, DOCTOR_NAME, DEPARTMENT_NAME,
            APPOINTMENT_DATE, APPOINTMENT_TIME
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            WHERE APPOINTMENT_STATUS = 'Pending'
            ORDER BY APPOINTMENT_DATE
        """,
    )

    run_query(
        cursor,
        "Q6: Unpaid Bills",
        f"""
            SELECT PATIENT_NAME, DOCTOR_NAME, DEPARTMENT_NAME,
            BILL_AMOUNT, PAYMENT_STATUS
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            WHERE PAYMENT_STATUS = 'Unpaid'
            ORDER BY BILL_AMOUNT DESC
        """,
    )

    run_query(
        cursor,
        "Q7: City-wise Patient Visits",
        f"""
            SELECT PATIENT_CITY,
            COUNT(APPOINTMENT_ID) AS TOTAL_NUMBER_OF_APPOINTMENTS
            FROM {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS
            GROUP BY PATIENT_CITY
            ORDER BY TOTAL_NUMBER_OF_APPOINTMENTS DESC
        """,
    )

    run_query(
        cursor,
        "FINAL: V_DEPARTMENT_DAILY_REVENUE View",
        f"""
            SELECT * FROM {SCHEMA}.V_DEPARTMENT_DAILY_REVENUE
            ORDER BY APPOINTMENT_DATE, DEPARTMENT_NAME
        """,
    )