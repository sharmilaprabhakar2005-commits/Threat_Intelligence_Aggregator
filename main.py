from modules.parser import fetch_url_feed
from modules.normalizer import normalize_iocs
from modules.correlator import correlate_iocs
from modules.blocklist_generator import generate_blocklists
from modules.reporter import generate_report, save_report
from modules.risk_engine import calculate_risk_score


# -------------------------
# SAMPLE IOC FEED (fallback)
# -------------------------
def load_sample_data():

    return [
        {"type": "ip", "value": "192.168.1.1"},
        {"type": "ip", "value": "10.0.0.1"},
        {"type": "domain", "value": "malicious.com"},
        {"type": "url", "value": "http://badsite.com/login"},
        {"type": "hash", "value": "5f4dcc3b5aa765d61d8327deb882cf99"},
        {"type": "ip", "value": "192.168.1.1"},
    ]


# -------------------------
# STEP 1: LIVE OSINT FEEDS
# -------------------------
def load_live_feed():

    urls = [
        "https://urlhaus.abuse.ch/downloads/text/",
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"
    ]

    all_iocs = []

    print("[+] Fetching real OSINT feeds...")

    for url in urls:

        print(f"[+] Connecting: {url}")

        try:
            data = fetch_url_feed(url)
            all_iocs.extend(data)
            print(f"[+] Loaded {len(data)} indicators from feed")

        except Exception as e:
            print("[ERROR] Failed feed:", url)
            print("Reason:", e)

    return all_iocs


# -------------------------
# MAIN PIPELINE (STEP 1 + 2 + 3)
# -------------------------
def main():

    print("\n[+] Threat Intelligence Aggregator Started\n")

    # =========================
    # STEP 1: DATA INGESTION
    # =========================
    raw_local = load_sample_data()
    raw_live = load_live_feed()

    raw_iocs = raw_local + raw_live
    print("[+] Total Raw IOCs:", len(raw_iocs))

    # =========================
    # STEP 2: NORMALIZATION
    # =========================
    normalized = normalize_iocs(raw_iocs, "combined_feed")
    print("[+] Normalized IOCs:", len(normalized))

    # =========================
    # STEP 3: CORRELATION
    # =========================
    correlated = correlate_iocs(normalized)
    print("[+] Correlated IOCs:", len(correlated))

    # =========================
    # STEP 4: BLOCKLIST GENERATION
    # =========================
    blocklists = generate_blocklists(normalized)
    print("[+] Blocklists created")

    # =========================
    # STEP 5: REPORT GENERATION
    # =========================
    report = generate_report(normalized, correlated, blocklists)
    save_report(report)
    print("[+] Report saved to output/report.json")

    # =========================
    # STEP 6: RISK SCORING (STEP 3 ENHANCEMENT)
    # =========================
    scored = calculate_risk_score(normalized, correlated)

    print("\n[+] Top 5 High Risk IOCs:")
    for item in scored[:5]:
        print(item)

    print("\n[+] Threat Intelligence Aggregator Completed Successfully\n")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    main()