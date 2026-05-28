import requests
import ipaddress

# -------------------------
# GEOIP LOOKUP MODULE
# -------------------------
def get_geoip(ip):

    try:
        ipaddress.ip_address(ip)

        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        return {
            "ip": ip,
            "country": data.get("country"),
            "region": data.get("regionName"),
            "isp": data.get("isp")
        }

    except:
        return {
            "ip": ip,
            "country": "Unknown",
            "region": "Unknown",
            "isp": "Unknown"
        }