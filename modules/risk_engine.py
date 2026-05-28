from collections import defaultdict

def calculate_risk_score(normalized_iocs, correlated_data):

    score_map = {
        "ip": 2,
        "domain": 2,
        "url": 3,
        "hash": 4,
        "email": 1
    }

    frequency = defaultdict(int)

    for item in normalized_iocs:
        frequency[item["value"]] += 1

    results = []

    for ioc in normalized_iocs:

        value = ioc["value"]
        ioc_type = ioc["type"]

        score = score_map.get(ioc_type, 1)

        if frequency[value] > 1:
            score += 3

        if "abuse" in ioc.get("source", ""):
            score += 2

        results.append({
            "type": ioc_type,
            "value": value,
            "source": ioc.get("source", ""),
            "risk_score": score
        })

    return sorted(results, key=lambda x: x["risk_score"], reverse=True)