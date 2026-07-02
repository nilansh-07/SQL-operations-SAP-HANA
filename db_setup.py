import os
from dotenv import load_dotenv
from hdbcli import dbapi

load_dotenv()
SCHEMA = os.getenv("HANA_SCHEMA")

def _get_fallback_schema(cursor):
    try:
        cursor.execute("SELECT CURRENT_SCHEMA FROM DUMMY")
        current_schema = cursor.fetchone()[0]
    except Exception:
        current_schema = None

    try:
        cursor.execute("SELECT CURRENT_USER FROM DUMMY")
        current_user = cursor.fetchone()[0]
    except Exception:
        current_user = None

    if current_schema:
        print(f"HANA_SCHEMA is not set. Defaulting to CURRENT_SCHEMA: {current_schema}")
        return current_schema
    
    if current_schema:
        print(f"HANA_SCHEMA is not set and CURRENT_SCHEMA is unavailable. Defaulting to CURRENT_USER: {current_user}")
        return current_user
    raise RuntimeError("Unable to determine schema name from HANA_SCHEMA or current session")


def _quote_name(name):
    return f'"{name}"'

def _qualified_name(schema_name, object_name):
    return f"{_quote_name(schema_name)}.{_quote_name(object_name)}"

def _print_debug_context(cursor):
    print("\n --- DEBUG CONTEXT ---")
    print(f"SCHEMA constant value: {SCHEMA}")
    for label, query in [
        ("CURRENT_USER", "SELECT CURRENT_USER FROM DUMMY"),
        ("CURRENT_SCHEMA", "SELECT CURRENT_SCHEMA FROM DUMMY"),
    ]:
        try:
            cursor.execute(query)
            value = cursor.fetchone()[0]
            print(f"{label} : {value}")
        except Exception as exc:
            print(f"Could not query {label} : {repr(exc)}")

    schema_name = SCHEMA
    if schema_name is None:
        schema_name = _get_fallback_schema(cursor)
    try:
        cursor.execute(f"SELECT SCHEMA_OWNER FROM SYS.SCHEMAS WHERE SCHEMA_NAME = '{schema_name}'")
        row = cursor.fetchone()
        print(f"Schema owner for {schema_name} : {row[0] if row else 'Not Found'}")
    except Exception as exc:
        print(f"Could not query schema owner for {schema_name} : {repr(exc)}")

    print("--- END DEBUG CONTEXT ---\n")


def _execute_sql(cursor, stmt):
    cleaned = stmt.strip()
    print(f"Executing SQL:\n{cleaned}\n")
    try:
        cursor.execute(cleaned)
    except Exception as exc:
        print("Full exception:", repr(exc))
        raise

def _is_already_exists_error(exc):
    text = str(exc).lower()
    return (
        "already exists" in text
        or "duplicate schema name" in text
        or ("exists" in text and "schema" in text)
        or ("already exists" in text and "table" in text)
    )

def _is_object_not_found_error(exc):
    if hasattr(exc, "errorcode") and exc.errorcode == 259:
        return True
    text = str(exc).lower()
    return (
        "does not exist" in text
        or "not exist" in text
        or "object does not exist" in text
        or "invalid table name" in text
    )

def _is_insufficient_privilege_error(exc):
    text = str(exc).lower()
    if "insufficient privilege" in text:
        return True
    if hasattr(exc, "errorcode") and exc.errorcode == 258:
        return True
    return False

def setup_schema_and_tables(cursor):
    print("=" * 60)
    print("STEP 1: CREATING SCHEMA AND TABLES")
    print("=" * 60)

    _print_debug_context(cursor)

    schema_name = SCHEMA or _get_fallback_schema(cursor)
    print(f"Using schema: {schema_name}")

    try:
        _execute_sql(cursor, f"CREATE SCHEMA {_quote_name(schema_name)}")
        print(f"Schema {schema_name} created.")
    except Exception as exc:
        if _is_already_exists_error(exc):
            print(f"Schema {schema_name} already exists.")
        elif _is_insufficient_privilege_error(exc):
            print(f"Permission error creating schema {schema_name}")
            raise
        else:
            print(f"Failed to create schema {schema_name}.")
            raise

        _execute_sql(cursor, f"SET SCHEMA {_quote_name(schema_name)}")

        tables_to_drop = ["BILLING", "APPOINTMENTS", "DOCTORS", "PATIENTS", "DEPARTMENTS"]
        for table in tables_to_drop:
            try:
                _execute_sql(cursor, f"DROP TABLE {_quote_name(table)}")
                print(f"Dropped table: {table}")
            except Exception as exc:
                if _is_object_not_found_error(exc):
                    print(f"Table {_quote_name(table)} does not exist. Skipping drop.")
                elif _is_insufficient_privilege_error(exc):
                    print(f"Permission error dropping table {_quote_name(table)}.")
                    raise
                else:
                    raise

        stmts = [
            (
                "PATIENTS",
                f"""
                    CREATE COLUMN TABLE {_quote_name('PATIENTS')} (
                        PATIENT_ID INTEGER PRIMARY KEY,
                        PATIENT_NAME NVARCHAR(100) NOT NULL,
                        GENDER NVARCHAR(10),
                        AGE INTEGER,
                        CITY NVARCHAR(50),
                        MOBILE_NUMBER NVARCHAR(15)
                    )
                """,
            ),
            (
                "DEPARTMENTS",
                f"""
                    CREATE COLUMN TABLE {_quote_name('DEPARTMENTS')} (
                        DEPARTMENT_ID INTEGER PRIMARY KEY,
                        DEPARTMENT_NAME NVARCHAR(50) NOT NULL,
                        FLOOR_NUMBER INTEGER
                    )
                """,
            ),
            (
                "DOCTORS",
                f"""
                   CREATE COLUMN TABLE {_quote_name('DOCTORS')} (
                    DOCTOR_ID INTEGER PRIMARY KEY,
                    DOCTOR_NAME NVARCHAR(100) NOT NULL,
                    DEPARTMENT_ID INTEGER NOT NULL,
                    SPECIALIZATION NVARCHAR(50),
                    CONSULTATION_FEE DECIMAL(10, 2),
                    FOREIGN KEY (DEPARTMENT_ID) REFERENCES {_quote_name('DEPARTMENTS')}(DEPARTMENT_ID)
                   )
                """,
            ),
            (
                "APPOINTMENTS",
                f"""
                CREATE COLUMN TABLE {_quote_name('APPOINTMENTS')} (
                    APPOINTMENT_ID INTEGER PRIMARY KEY,
                    PATIENT_ID INTEGER NOT NULL,
                    DOCTOR_ID INTEGER NOT NULL,
                    APPOINTMENT_DATE DATE,
                    APPOINTMENT_TIME TIME,
                    APPOINTMENT_STATUS NVARCHAR(20) NOT NULL,
                    FOREIGN KEY (PATIENT_ID) REFERENCES {_quote_name('PATIENTS')}(PATIENT_ID),
                    FOREIGN KEY (DOCTOR_ID) REFERENCES {_quote_name('DOCTORS')}(DOCTOR_ID)
                )
                """,
            ),
            (
                "BILLING",
                f"""
                    CREATE COLUMN TABLE {_quote_name('BILLING')} (
                    BILL_ID INTEGER PRIMARY KEY,
                    APPOINTMENT_ID INTEGER NOT NULL UNIQUE,
                    BILL_AMOUNT DECIMAL(10, 2),
                    PAYMENT_MODE NVARCHAR(20),
                    PAYMENT_STATUS NVARCHAR(20),
                    FOREIGN KEY (APPOINTMENT_ID) REFERENCES {_quote_name('APPOINTMENTS')}(APPOINTMENT_ID)
                    )
                """,
            ),
        ]

        for name, stmt in stmts:
            try:
                _execute_sql(cursor, stmt)
                print(f"Created table: {name}")
            except Exception as exc:
                if _is_insufficient_privilege_error(exc):
                    print(f"Permission error creating table {name} in schema {schema_name}")
                else:
                    print(f"Failed to create table {name} in schema {schema_name}.")
                raise
            
        print(f"\nAll 5 tables created successfully in schema {schema_name}")

