import requests

url = "https://ai-calling-agent-9hv2.onrender.com/call"
payload = {
    "to_number": "+13104211169"
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
