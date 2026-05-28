import json
import csv
import requests

# ✅ IMPORT VALIDATOR (STEP 2 FIX)
from modules.validator import is_valid_ioc


# -------------------------
# TXT PARSER (CLEANED)
# -------------------------
def parse_txt(file_path):

    indicators = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        for line in file:
            value = line.strip()

            # ✅ STEP 2: validate before adding
            if is_valid_ioc(value):

                indicators.append({
                    "type": "unknown",
                    "value": value
                })

    return indicators


# -------------------------
# CSV PARSER (CLEANED)
# -------------------------
def parse_csv(file_path):

    indicators = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        reader = csv.DictReader(file)

        for row in reader:

            value = row.get("value", "").strip()
            ioc_type = row.get("type", "unknown").strip()

            # validate IOC
            if is_valid_ioc(value):

                indicators.append({
                    "type": ioc_type,
                    "value": value
                })

    return indicators


# -------------------------
# JSON PARSER (CLEANED)
# -------------------------
def parse_json(file_path):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        data = json.load(file)

    cleaned = []

    for item in data:

        value = item.get("value", "").strip()

        if is_valid_ioc(value):

            cleaned.append({
                "type": item.get("type", "unknown"),
                "value": value
            })

    return cleaned


# -------------------------
# STEP 1 + STEP 2 UPGRADE: LIVE FEED FETCHER (CLEANED)
# -------------------------
def fetch_url_feed(url):

    indicators = []

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        lines = response.text.splitlines()

        for line in lines:

            value = line.strip()

            # ❌ remove junk BEFORE adding
            if not value:
                continue

            if value.startswith("#"):
                continue

            # ✅ STEP 2 validation
            if is_valid_ioc(value):

                indicators.append({
                    "type": "unknown",
                    "value": value,
                    "source": url
                })

    except Exception as e:
        print("[ERROR] Failed to fetch feed:", url)
        print("Reason:", e)

    return indicators