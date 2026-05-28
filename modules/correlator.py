from collections import defaultdict

# -------------------------
# IOC CORRELATION ENGINE
# -------------------------
def correlate_iocs(iocs):

    correlation = defaultdict(list)

    # Group by indicator value
    for ioc in iocs:
        correlation[ioc["value"]].append(ioc["source"])

    results = []

    for value, sources in correlation.items():

        unique_sources = list(set(sources))
        count = len(unique_sources)

        # Severity logic
        if count >= 3:
            severity = "Critical"
        elif count == 2:
            severity = "High"
        else:
            severity = "Low"

        results.append({
            "indicator": value,
            "sources": unique_sources,
            "count": count,
            "severity": severity
        })

    return results