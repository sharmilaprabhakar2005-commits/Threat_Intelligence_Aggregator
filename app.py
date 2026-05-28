from flask import Flask, render_template, jsonify, send_file
from flask_socketio import SocketIO
from reportlab.pdfgen import canvas

import datetime
import csv
import os

from feed_parser import fetch_url_feed
from normalizer import normalize_iocs
from correlator import correlate_iocs
from risk_engine import calculate_risk_score

app = Flask(**name**)

# SocketIO Configuration

socketio = SocketIO(
app,
cors_allowed_origins="*",
async_mode="eventlet"
)

def build_pipeline():

```
urls = [
    "https://urlhaus.abuse.ch/downloads/text/",
    "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"
]

raw = []

for url in urls:
    try:
        raw.extend(fetch_url_feed(url))
    except Exception as e:
        print(f"Feed Error: {e}")

normalized = normalize_iocs(raw, "live_dashboard")
correlated = correlate_iocs(normalized)
scored = calculate_risk_score(normalized, correlated)

return scored
```

@app.route("/")
def dashboard():
return render_template("dashboard.html")

@app.route("/api/iocs")
def api_iocs():

```
try:
    data = build_pipeline()

    socketio.emit("ioc_update", data)

    return jsonify(data)

except Exception as e:
    return jsonify({
        "error": str(e)
    }), 500
```

@app.route("/api/stats")
def api_stats():

```
try:
    data = build_pipeline()

    return jsonify({
        "total": len(data),
        "high": len([
            i for i in data
            if i.get("risk_score", 0) >= 4
        ]),
        "medium": len([
            i for i in data
            if i.get("risk_score", 0) == 3
        ]),
        "low": len([
            i for i in data
            if i.get("risk_score", 0) <= 2
        ]),
    })

except Exception as e:
    return jsonify({
        "error": str(e)
    }), 500
```

@app.route("/api/timeline")
def api_timeline():

```
try:
    data = build_pipeline()

    timeline = []

    for ioc in data:
        timeline.append({
            "type": ioc.get("type"),
            "risk": ioc.get("risk_score", 0),
            "source": ioc.get("source", "unknown")
        })

    return jsonify(timeline)

except Exception as e:
    return jsonify({
        "error": str(e)
    }), 500
```

@app.route("/export/pdf")
def export_pdf():

```
try:

    data = build_pipeline()

    os.makedirs("output", exist_ok=True)

    file_path = "output/soc_report.pdf"

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 800, "SOC THREAT INTELLIGENCE REPORT")

    c.setFont("Helvetica", 10)
    c.drawString(
        180,
        780,
        f"Generated: {datetime.datetime.now()}"
    )

    total = len(data)

    high = len([
        i for i in data
        if i.get("risk_score", 0) >= 4
    ])

    medium = len([
        i for i in data
        if i.get("risk_score", 0) == 3
    ])

    low = len([
        i for i in data
        if i.get("risk_score", 0) <= 2
    ])

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

        if y < 50:
            c.showPage()
            y = 800

    c.save()

    return send_file(
        file_path,
        as_attachment=True
    )

except Exception as e:
    return jsonify({
        "error": str(e)
    }), 500
```

@app.route("/export/csv")
def export_csv():

```
try:

    data = build_pipeline()

    os.makedirs("output", exist_ok=True)

    file_path = "output/report.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

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

    return send_file(
        file_path,
        as_attachment=True
    )

except Exception as e:
    return jsonify({
        "error": str(e)
    }), 500
```

@app.route("/logout")
def logout():
return "<h2>Logged Out Successfully</h2>"

# MAIN ENTRY POINT

if **name** == "**main**":

```
port = int(os.environ.get("PORT", 10000))

socketio.run(
    app,
    host="0.0.0.0",
    port=port,
    debug=False
)
```
