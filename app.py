
from flask import Flask, render_template, jsonify, send_file
from flask_socketio import SocketIO
from reportlab.pdfgen import canvas

import datetime
import csv

from modules.parser import fetch_url_feed
from modules.normalizer import normalize_iocs
from modules.correlator import correlate_iocs
from modules.risk_engine import calculate_risk_score

app = Flask(__name__)

# =========================
# SOCKET INIT (STEP 3)
# =========================
socketio = SocketIO(app, cors_allowed_origins="*")


# =========================
# PIPELINE ENGINE
# =========================
def build_pipeline():

    urls = [
        "https://urlhaus.abuse.ch/downloads/text/",
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"
    ]

    raw = []

    for url in urls:
        try:
            raw.extend(fetch_url_feed(url))
        except:
            pass

    normalized = normalize_iocs(raw, "live_dashboard")
    correlated = correlate_iocs(normalized)
    scored = calculate_risk_score(normalized, correlated)

    return scored


# =========================
# DASHBOARD PAGE
# =========================
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# =========================
# LIVE IOC API + SOCKET PUSH
# =========================
@app.route("/api/iocs")
def api_iocs():

    data = build_pipeline()

    # REAL-TIME PUSH
    socketio.emit("ioc_update", data)

    return jsonify(data)


# =========================
# STATS API
# =========================
@app.route("/api/stats")
def api_stats():

    data = build_pipeline()

    return jsonify({
        "total": len(data),
        "high": len([i for i in data if i.get("risk_score", 0) >= 4]),
        "medium": len([i for i in data if i.get("risk_score", 0) == 3]),
        "low": len([i for i in data if i.get("risk_score", 0) <= 2]),
    })


# =========================
# ATTACK TIMELINE API
# =========================
@app.route("/api/timeline")
def api_timeline():

    data = build_pipeline()

    timeline = []

    for ioc in data:
        timeline.append({
            "type": ioc.get("type"),
            "risk": ioc.get("risk_score", 0),
            "source": ioc.get("source", "unknown")
        })

    return jsonify(timeline)


# =========================
# PDF EXPORT
# =========================
@app.route("/export/pdf")
def export_pdf():

    data = build_pipeline()

    file_path = "output/soc_report.pdf"

    c = canvas.Canvas(file_path)

    # HEADER
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 800, "SOC THREAT INTELLIGENCE REPORT")

    c.setFont("Helvetica", 10)
    c.drawString(180, 780, f"Generated: {datetime.datetime.now()}")

    # SUMMARY
    total = len(data)
    high = len([i for i in data if i.get("risk_score", 0) >= 4])
    medium = len([i for i in data if i.get("risk_score", 0) == 3])
    low = len([i for i in data if i.get("risk_score", 0) <= 2])

    y = 740

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "SUMMARY")

    y -= 20
    c.setFont("Helvetica", 10)

    c.drawString(50, y, f"Total IOCs: {total}")
    y -= 15

    c.drawString(50, y, f"High Risk: {high}")
    y -= 15

    c.drawString(50, y, f"Medium Risk: {medium}")
    y -= 15

    c.drawString(50, y, f"Low Risk: {low}")

    # TOP IOCS
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TOP HIGH RISK IOCs")

    y -= 20
    c.setFont("Helvetica", 9)

    sorted_data = sorted(
        data,
        key=lambda x: x.get("risk_score", 0),
        reverse=True
    )

    for ioc in sorted_data[:25]:

        text = (
            f"{ioc.get('type')} | "
            f"{ioc.get('value')} | "
            f"Risk: {ioc.get('risk_score')}"
        )

        c.drawString(50, y, text)

        y -= 15

        # PAGE BREAK
        if y < 50:
            c.showPage()
            y = 800

    c.save()

    return send_file(file_path, as_attachment=True)


# =========================
# CSV EXPORT
# =========================
@app.route("/export/csv")
def export_csv():

    data = build_pipeline()

    file_path = "output/report.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Type",
            "Value",
            "Risk Score",
            "Source"
        ])

        for ioc in data:

            writer.writerow([
                ioc.get("type"),
                ioc.get("value"),
                ioc.get("risk_score"),
                ioc.get("source")
            ])

    return send_file(file_path, as_attachment=True)


# =========================
# LOGOUT ROUTE
# =========================
@app.route("/logout")
def logout():
    return "<h2>Logged Out Successfully</h2>"


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    socketio.run(app, debug=True)

