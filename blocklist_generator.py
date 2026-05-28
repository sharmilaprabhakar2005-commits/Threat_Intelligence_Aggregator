# -------------------------
# BLOCKLIST GENERATOR
# -------------------------

def generate_blocklists(iocs):

    ip_list = []
    domain_list = []
    hash_list = []
    url_list = []

    for ioc in iocs:

        ioc_type = ioc["type"]
        value = ioc["value"]

        if ioc_type == "ip":
            ip_list.append(value)

        elif ioc_type == "domain":
            domain_list.append(value)

        elif ioc_type == "hash":
            hash_list.append(value)

        elif ioc_type == "url":
            url_list.append(value)

    return {
        "ips": list(set(ip_list)),
        "domains": list(set(domain_list)),
        "hashes": list(set(hash_list)),
        "urls": list(set(url_list))
    }