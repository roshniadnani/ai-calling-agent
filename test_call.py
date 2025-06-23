import requests

url = "https://ai-calling-agent-9hv2.onrender.com/call"  # Make sure this is correct
payload = {"to_number": "+13104211169"}

print(f"📞 Initiating outbound call to: {payload['to_number']}")
response = requests.post(url, json=payload)

print(f"🔹 Status: {response.status_code}")
print(f"🔹 Response: {response.text}")
