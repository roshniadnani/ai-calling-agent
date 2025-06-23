import requests

# Replace this with your deployed Render base URL
BASE_URL = "https://ai-calling-agent-9hv2.onrender.com"

# Number to call
to_number = "+13104211169"

try:
    print("📞 Initiating outbound call to:", to_number)
    
    response = requests.post(
        f"{BASE_URL}/call",
        json={"to_number": to_number}
    )

    print("🔹 Status:", response.status_code)
    print("🔹 Headers:", response.headers)
    print("🔹 Body:", repr(response.text))

    if response.status_code == 200:
        print("✅ Call trigger successful.")
    else:
        print("❌ Failed to trigger call.")
except Exception as e:
    print(f"❌ Error during request: {e}")
