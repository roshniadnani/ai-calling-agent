import requests

# Define the URL of your deployed app
url = "https://ai-calling-agent-9hv2.onrender.com/call"

# The phone number you're calling (MUST be whitelisted in Vonage test list)
data = {
    "to": "+13104211169"  # Replace this if needed
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

print("📞 Initiating outbound call to:", data["to"])
print("🔹 Status:", response.status_code)
print("🔹 Response:", response.text)
