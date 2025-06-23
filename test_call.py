import requests

url = "https://ai-calling-agent-9hv2.onrender.com/call"
payload = {"to_number": "+13104211169"}

print(f"📞 Initiating outbound call to: {payload['to_number']}")
res = requests.post(url, json=payload)

print(f"🔹 Status: {res.status_code}")
print(f"🔹 Headers: {res.headers}")
print(f"🔹 Body: {res.text}")

if res.status_code == 200:
    print("✅ Call trigger successful.")
else:
    print("❌ Failed to trigger call.")
