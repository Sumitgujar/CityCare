import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "citycare.db")


def get_db_connection():
    """Returns a new SQLite connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist and seed sample data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # ── Appointments table ──────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name        TEXT    NOT NULL,
            phone            TEXT    NOT NULL,
            email            TEXT,
            age              TEXT,
            gender           TEXT,
            blood_group      TEXT,
            doctor           TEXT    NOT NULL,
            department       TEXT,
            appointment_date TEXT    NOT NULL,
            appointment_time TEXT    NOT NULL,
            reason           TEXT,
            status           TEXT    DEFAULT 'Pending',
            created_at       TEXT    NOT NULL
        )
    """)

    # ── Doctors table ───────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            speciality   TEXT NOT NULL,
            experience   TEXT,
            availability TEXT,
            is_active    INTEGER DEFAULT 1
        )
    """)

    # ── Contact messages table ──────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT,
            email      TEXT,
            subject    TEXT,
            message    TEXT,
            created_at TEXT
        )
    """)

    # ── Seed doctors (only if table is empty) ───────────────────────────
    if cursor.execute("SELECT COUNT(*) FROM doctors").fetchone()[0] == 0:
        doctors_seed = [
            ("Dr. Rajesh Mehta",  "Cardiologist",       "15 years", "Mon–Fri, 9AM–2PM"),
            ("Dr. Sneha Patil",   "Pediatrician",       "10 years", "Mon–Sat, 10AM–4PM"),
            ("Dr. Amit Kumar",    "Orthopedic Surgeon", "12 years", "Tue–Sat, 11AM–5PM"),
            ("Dr. Priya Desai",   "Neurologist",        "8 years",  "Mon–Thu, 9AM–1PM"),
            ("Dr. Suresh Nair",   "Ophthalmologist",    "9 years",  "Mon–Fri, 2PM–6PM"),
            ("Dr. Meena Joshi",   "Dental Surgeon",     "7 years",  "Tue–Sat, 9AM–3PM"),
        ]
        cursor.executemany(
            "INSERT INTO doctors (name, speciality, experience, availability) VALUES (?,?,?,?)",
            doctors_seed
        )

    # ── Seed sample appointments (only if table is empty) ───────────────
    if cursor.execute("SELECT COUNT(*) FROM appointments").fetchone()[0] == 0:
        from datetime import datetime, timedelta
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sample_appointments = [
            ("Priya Sharma",   "9876543210", "priya@email.com",  "28", "Female", "B+",
             "Dr. Rajesh Mehta",  "Cardiology",  today,    "9:00 AM",  "Chest pain",           "Confirmed", now),
            ("Ravi Kulkarni",  "9765432109", "ravi@email.com",   "45", "Male",   "O+",
             "Dr. Sneha Patil",   "Pediatrics",  today,    "10:30 AM", "Child fever",          "Pending",   now),
            ("Anita Joshi",    "9654321098", "anita@email.com",  "35", "Female", "A+",
             "Dr. Amit Kumar",    "Orthopedics", today,    "11:00 AM", "Knee pain",            "Confirmed", now),
            ("Suresh Nair",    "9543210987", "suresh@email.com", "52", "Male",   "AB+",
             "Dr. Priya Desai",   "Neurology",   today,    "2:00 PM",  "Frequent headaches",   "Pending",   now),
            ("Meena Patil",    "9432109876", "meena@email.com",  "30", "Female", "O-",
             "Dr. Rajesh Mehta",  "Cardiology",  tomorrow, "9:30 AM",  "Routine checkup",      "Confirmed", now),
            ("Vikram Rao",     "9321098765", "vikram@email.com", "60", "Male",   "B-",
             "Dr. Suresh Nair",   "Ophthalmology",tomorrow,"2:30 PM",  "Vision problems",      "Pending",   now),
        ]
        cursor.executemany("""
            INSERT INTO appointments
              (full_name, phone, email, age, gender, blood_group,
               doctor, department, appointment_date, appointment_time,
               reason, status, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, sample_appointments)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully → citycare.db")


if __name__ == "__main__":
    init_db()
