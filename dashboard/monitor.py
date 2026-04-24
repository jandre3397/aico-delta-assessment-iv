import requests

services = {
    "fraud-detection": "http://aa624e7c24e9b444e8e7b1463021c552-838256341.us-east-1.elb.amazonaws.com/health",
    "recommendations": "http://k8s-recommen-recommen-95023365a1-d56102cfb85e5314.elb.us-east-1.amazonaws.com/health",
    "forecasting": "http://k8s-forecast-forecast-7afea06d55-9e943ebbf45cd75f.elb.us-east-1.amazonaws.com/health",
}

for name, url in services.items():
    try:
        response = requests.get(url, timeout=5)
        print(f"\n{name}: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"\n{name}: unreachable - {e}")