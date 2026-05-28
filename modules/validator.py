import re
import ipaddress

# -------------------------
# IOC VALIDATION MODULE
# -------------------------

def is_valid_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except:
        return False


def is_valid_domain(value):
    pattern = r"^(?!-)[A-Za-z0-9-]+(\.[A-Za-z]{2,})+$"
    return bool(re.match(pattern, value))


def is_valid_url(value):
    pattern = r"^https?://"
    return bool(re.match(pattern, value))


def is_valid_hash(value):
    return bool(re.match(r"^[a-fA-F0-9]{32,64}$", value))


def is_valid_ioc(value):

    value = value.strip()

    # ignore comments / noise
    if value.startswith("#") or value == "":
        return False

    return (
        is_valid_ip(value) or
        is_valid_domain(value) or
        is_valid_url(value) or
        is_valid_hash(value)
    )