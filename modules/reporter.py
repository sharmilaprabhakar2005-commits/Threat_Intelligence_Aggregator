import json
from datetime import datetime

def generate_report(normalized_iocs, correlated_data, blocklists):

    report = {
        "timestamp": str(datetime.now()),
        "total_iocs": len(normalized_iocs),

        "severity_summary": {
            "Critical": 0,
            "High": 0,
            "Low": 0
        },

        "high_risk_indicators": [],
        "blocklists": blocklists
    }

    for item in correlated_data:

        severity = item["severity"]

        if severity in report["severity_summary"]:
            report["severity_summary"][severity] += 1

        if severity in ["Critical", "High"]:
            report["high_risk_indicators"].append(item)

    return report


def save_report(report, filename="output/report.json"):

    with open(filename, "w") as file:
        json.dump(report, file, indent=4)

    print("[+] Report saved to", filename)