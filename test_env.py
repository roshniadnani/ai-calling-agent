import os
from dotenv import load_dotenv

load_dotenv()

print("ELEVEN_API_KEY:", os.getenv("ELEVEN_API_KEY"))
print("DESIREE_AGENT_ID:", os.getenv("DESIREE_AGENT_ID"))
