import requests
import io
from PIL import Image

BASE_URL = "http://localhost:5000"

def run_tests():
    session = requests.Session()
    
    print("\n--- 1. SIGN IN ---")
    login_payload = {
        "email": "user@example.com",
        "password": "password"
    }
    resp = session.post(f"{BASE_URL}/signin", data=login_payload)
    if resp.status_code != 200 or "signin" in resp.url.lower():
        print("Registration needed. Signing up...")
        signup_payload = {
            "name": "Jahnavi Gongati",
            "email": "user@example.com",
            "password": "password",
            "confirm_password": "password"
        }
        session.post(f"{BASE_URL}/signup", data=signup_payload)
        resp = session.post(f"{BASE_URL}/signin", data=login_payload)
    
    print("Sign in status:", resp.status_code)
    
    print("\n--- 2. GENERATING DUMMY LEAF IMAGE ---")
    img = Image.new('RGB', (300, 300), color=(34, 139, 34)) # Forest Green leaf image
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    print("\n--- 3. TESTING /api/crop-analysis (Telugu) ---")
    files = {
        'image': ('test_leaf.png', img_byte_arr, 'image/png')
    }
    data = {
        'language': 'te'
    }
    
    resp = session.post(f"{BASE_URL}/api/crop-analysis", files=files, data=data)
    print("Upload status code:", resp.status_code)
    try:
        res_json = resp.json()
        print("Response keys:", res_json.keys())
        if res_json.get('success'):
            print("UPLOAD: PASS")
            print("GEMINI VISION CALL: PASS")
            print("ANALYSIS PARSING: PASS")
            analysis = res_json['analysis']
            print("Detected crop:", analysis.get('crop'))
            print("Detected issue:", analysis.get('detected_issue'))
            print("Severity:", analysis.get('severity'))
            print("Confidence:", analysis.get('confidence'))
            print("Explanation length:", len(analysis.get('explanation', '')))
        else:
            print("FLOW FAILED:", res_json.get('error'))
            print("UPLOAD/GEMINI VISION CALL: FAIL")
            return
    except Exception as e:
        print("JSON parsing error:", e)
        print("UPLOAD/GEMINI VISION CALL: FAIL")
        return

    print("\n--- 4. TESTING CROP DISEASE CHAT FOLLOW-UP (Telugu) ---")
    chat_payload = {
        "agent": "crop-disease",
        "message": "దీనికి నివారణ ఏమిటి?", # "What is the prevention/remedy for this?" in Telugu
        "language": "te"
    }
    resp = session.post(f"{BASE_URL}/api/agent-chat", json=chat_payload)
    print("Chat API status code:", resp.status_code)
    try:
        chat_json = resp.json()
        if chat_json.get('success'):
            print("CROP DISEASE CHAT: PASS")
            print("Multilingual (Telugu) Response:\n", chat_json.get('message'))
        else:
            print("CHAT FLOW FAILED:", chat_json.get('error'))
            print("CROP DISEASE CHAT: FAIL")
    except Exception as e:
        print("Chat JSON parsing error:", e)
        print("CROP DISEASE CHAT: FAIL")

if __name__ == "__main__":
    run_tests()
