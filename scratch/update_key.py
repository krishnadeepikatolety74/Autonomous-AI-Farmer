import getpass
import re

print("==================================================")
print("ElevenLabs API Key Update Utility")
print("==================================================")
print("The current key in .env appears to be the 'API Key ID' (which is 64 hex characters)")
print("instead of the actual secret 'API Key' (which starts with 'sk_' and is 32 or 51 characters).")
print("Please enter your actual secret API Key below.")
print("Your typing will be hidden for security.")
print("--------------------------------------------------")

val = getpass.getpass("Enter ELEVENLABS_API_KEY: ").strip()
if not val:
    print("Error: Key cannot be empty.")
    exit(1)

# Read existing .env
try:
    with open(".env", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = ""

# Replace or append key
if "ELEVENLABS_API_KEY=" in content:
    content = re.sub(r"ELEVENLABS_API_KEY\s*=\s*.*", f"ELEVENLABS_API_KEY={val}", content)
else:
    content += f"\nELEVENLABS_API_KEY={val}\n"

with open(".env", "w") as f:
    f.write(content)

print("\nSaved successfully to .env.")
