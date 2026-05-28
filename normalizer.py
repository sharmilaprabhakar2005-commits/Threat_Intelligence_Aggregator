from modules.validator import (
    is_valid_ip,
    is_valid_domain,
    is_valid_url,
    is_valid_hash
)

# -------------------------
# DETECT IOC TYPE
# -------------------------
def detect_type(value):

    value = value.strip()

    if is_valid_ip(value):
        return "ip"

    if is_valid_url(value):
        return "url"

    if is_valid_domain(value):
        return "domain"

    if is_valid_hash(value):
        return "hash"

    return "unknown"


# -------------------------
# NORMALIZE IOCS
# -------------------------
def normalize_iocs(iocs, source_name):

    normalized = []

    for item in iocs:

        value = item.get("value", "").strip()
        ioc_type = item.get("type", "unknown")

        if ioc_type == "unknown":
            ioc_type = detect_type(value)

        normalized.append({
            "type": ioc_type,
            "value": value.lower(),
            "source": source_name
        })

    return normalized