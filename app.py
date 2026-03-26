from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import init_db, get_db_connection
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "citycare_secret_key_2024"

# Initialize DB on startup
init_db()

# ─────────────────────────────────────────
#  PUBLIC ROUTES
# ─────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/booking")
def booking():
    return render_template("index.html", page="booking")

@app.route("/about")
def about():
    return render_template("index.html", page="about")

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return render_template("index.html", page="admin")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        # Simple hardcoded admin credentials (use hashed passwords in production)
        if username == "admin" and password == "citycare123":
            session["admin_logged_in"] = True
            return jsonify({"success": True})
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    return render_template("index.html", page="admin_login")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

# ─────────────────────────────────────────
#  APPOINTMENT API
# ─────────────────────────────────────────

@app.route("/api/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()

    required = ["full_name", "phone", "doctor", "appointment_date", "appointment_time"]
    for field in required:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing field: {field}"}), 400

    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO appointments
              (full_name, phone, email, age, gender, blood_group,
               doctor, department, appointment_date, appointment_time,
               reason, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
        """, (
            data["full_name"], data["phone"], data.get("email", ""),
            data.get("age", ""), data.get("gender", ""), data.get("blood_group", ""),
            data["doctor"], data.get("department", "General"),
            data["appointment_date"], data["appointment_time"],
            data.get("reason", ""), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        appt_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return jsonify({
            "success": True,
            "message": "Appointment booked successfully!",
            "appointment_id": appt_id
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/appointments", methods=["GET"])
def get_appointments():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    status_filter = request.args.get("status", "All")
    conn = get_db_connection()
    if status_filter == "All":
        rows = conn.execute(
            "SELECT * FROM appointments ORDER BY created_at DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM appointments WHERE status=? ORDER BY created_at DESC",
            (status_filter,)
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/appointments/<int:appt_id>", methods=["PATCH"])
def update_appointment(appt_id):
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ("Confirmed", "Cancelled", "Pending"):
        return jsonify({"error": "Invalid status"}), 400

    conn = get_db_connection()
    conn.execute(
        "UPDATE appointments SET status=? WHERE id=?", (new_status, appt_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "status": new_status})


@app.route("/api/appointments/<int:appt_id>", methods=["DELETE"])
def delete_appointment(appt_id):
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    conn.execute("DELETE FROM appointments WHERE id=?", (appt_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


# ─────────────────────────────────────────
#  DASHBOARD STATS API
# ─────────────────────────────────────────

@app.route("/api/stats", methods=["GET"])
def get_stats():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    today = datetime.now().strftime("%Y-%m-%d")
    total       = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
    today_count = conn.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date=?", (today,)).fetchone()[0]
    pending     = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Pending'").fetchone()[0]
    confirmed   = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Confirmed'").fetchone()[0]
    conn.close()
    return jsonify({
        "total": total,
        "today": today_count,
        "pending": pending,
        "confirmed": confirmed
    })


# ─────────────────────────────────────────
#  CONTACT API
# ─────────────────────────────────────────

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO contact_messages (name, email, subject, message, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("name", ""), data.get("email", ""),
        data.get("subject", ""), data.get("message", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Message received! We'll get back to you soon."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
