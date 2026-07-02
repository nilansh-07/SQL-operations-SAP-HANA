import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("HANA_SCHEMA")


def create_views(cursor):
    print("\n" + "=" * 60)
    print("STEP 3: CREATING VIEWS")
    print("=" * 60)

    try:
        cursor.execute(f"DROP VIEW {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS")
    except Exception:
        pass

    cursor.execute(f"""
        CREATE VIEW {SCHEMA}.V_OPD_APPOINTMENT_ANALYTICS AS
        SELECT 
            A.APPOINTMENT_ID,
            A.APPOINTMENT_DATE,
            A.APPOINTMENT_TIME,
            P.PATIENT_NAME,
            P.CITY AS PATIENT_CITY,
            D.DOCTOR_NAME,
            DEP.DEPARTMENT_NAME,
            D.SPECIALIZATION,
            D.CONSULTATION_FEE,
            B.BILL_AMOUNT,
            B.PAYMENT_MODE,
            B.PAYMENT_STATUS,
            A.APPOINTMENT_STATUS
        FROM {SCHEMA}.APPOINTMENTS A
        INNER JOIN {SCHEMA}.PATIENTS P
            ON A.PATIENT_ID = P.PATIENT_ID
        INNER JOIN {SCHEMA}.DOCTORS D
            ON A.DOCTOR_ID = D.DOCTOR_ID
        INNER JOIN {SCHEMA}.DEPARTMENTS DEP
            ON D.DEPARTMENT_ID = DEP.DEPARTMENT_ID
        LEFT JOIN {SCHEMA}.BILLING B
            ON A.APPOINTMENT_ID = B.APPOINTMENT_ID
    """)
    print("Created view: V_OPD_APPOINTMENT_ANALYTICS")

    try:
        cursor.execute(f"DROP VIEW {SCHEMA}.V_DEPARTMENT_DAILY_REVENUE")
    except Exception:
        pass

    cursor.execute(f"""
        CREATE VIEW {SCHEMA}.V_DEPARTMENT_DAILY_REVENUE AS
        SELECT 
            A.APPOINTMENT_DATE,
            DEP.DEPARTMENT_NAME,
            COUNT(DISTINCT A.APPOINTMENT_ID) AS TOTAL_APPOINTMENTS,
            COUNT(DISTINCT B.BILL_ID) AS TOTAL_PAID_BILLS,
            COALESCE(SUM(B.BILL_AMOUNT), 0) AS TOTAL_REVENUE
        FROM {SCHEMA}.APPOINTMENTS A
        INNER JOIN {SCHEMA}.DOCTORS D
            ON A.DOCTOR_ID = D.DOCTOR_ID
        INNER JOIN {SCHEMA}.DEPARTMENTS DEP
            ON D.DEPARTMENT_ID = DEP.DEPARTMENT_ID
        LEFT JOIN {SCHEMA}.BILLING B
            ON A.APPOINTMENT_ID = B.APPOINTMENT_ID
            AND B.PAYMENT_STATUS = 'Paid'
        WHERE A.APPOINTMENT_STATUS = 'Completed'
        GROUP BY A.APPOINTMENT_DATE, DEP.DEPARTMENT_NAME
    """)
    print("Created view: V_DEPARTMENT_DAILY_REVENUE")

    print("\nBoth views created successfully.")