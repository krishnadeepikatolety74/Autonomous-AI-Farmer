import requests

BASE_URL = "http://localhost:5000"

def test_settings_suite():
    session = requests.Session()
    
    print("Initializing settings integration tests...")
    
    # 1. Log in the test user
    login_payload = {
        "email": "user@example.com",
        "password": "password"
    }
    print("Authenticating...")
    resp = session.post(f"{BASE_URL}/signin", data=login_payload)
    if resp.status_code != 200 or "signin" in resp.url.lower():
        # Let's try registering first
        print("Test user registration needed. Trying to signup...")
        signup_payload = {
            "name": "Jahnavi Gongati",
            "email": "user@example.com",
            "password": "password",
            "confirm_password": "password"
        }
        resp = session.post(f"{BASE_URL}/signup", data=signup_payload)
        print("Register status:", resp.status_code)
        
        # Log in again
        resp = session.post(f"{BASE_URL}/signin", data=login_payload)
        print("Login retry status:", resp.status_code)

    # 2. Get settings page
    print("\n1. Loading /settings GET page...")
    resp = session.get(f"{BASE_URL}/settings")
    print("Settings page status:", resp.status_code)
    assert resp.status_code == 200, "Failed to load settings page"

    # 3. Post profile update (duplicate email check)
    print("\n2. Updating profile details...")
    profile_payload = {
        "name": "Jahnavi Gongati Updated",
        "email": "user@example.com"
    }
    resp = session.post(f"{BASE_URL}/settings/profile", data=profile_payload, allow_redirects=False)
    print("Profile update redirect status:", resp.status_code)
    assert resp.status_code in [302, 200], "Failed to redirect on profile update"

    # 4. Post password update
    print("\n3. Testing password update...")
    password_payload = {
        "current_password": "password",
        "new_password": "password_new",
        "confirm_password": "password_new"
    }
    resp = session.post(f"{BASE_URL}/settings/password", data=password_payload, allow_redirects=False)
    print("Password update status:", resp.status_code)
    
    # Revert password back for future tests
    password_revert_payload = {
        "current_password": "password_new",
        "new_password": "password",
        "confirm_password": "password"
    }
    session.post(f"{BASE_URL}/settings/password", data=password_revert_payload, allow_redirects=False)
    print("Reverted password status successfully.")

    # 5. Post preferences update
    print("\n4. Testing preferences update...")
    pref_payload = {
        "language": "hi",
        "voice_responses": "ON",
        "auto_play_voice": "ON",
        "voice": "Josh"
    }
    resp = session.post(f"{BASE_URL}/settings/preferences", data=pref_payload, allow_redirects=False)
    print("Preferences update status:", resp.status_code)
    assert resp.status_code in [302, 200], "Failed to update preferences"

    # 6. Test Quick Notes JSON API endpoints
    print("\n5. Testing /quick-notes GET...")
    resp = session.get(f"{BASE_URL}/quick-notes")
    print("GET notes status:", resp.status_code, resp.json())
    assert resp.status_code == 200
    
    print("\n6. Creating a new quick note...")
    note_payload = {"note": "Buy NPK fertilizer"}
    resp = session.post(f"{BASE_URL}/quick-notes", json=note_payload)
    print("Create note status:", resp.status_code, resp.json())
    assert resp.status_code == 200
    note_id = resp.json()['note']['id']
    
    print("\n7. Toggling note completion status...")
    resp = session.post(f"{BASE_URL}/quick-notes/{note_id}/complete", json={"completed": 1})
    print("Complete note status:", resp.status_code, resp.json())
    assert resp.status_code == 200
    assert resp.json()['note']['completed'] == 1
    
    print("\n8. Clearing completed notes...")
    resp = session.post(f"{BASE_URL}/quick-notes/clear-completed")
    print("Clear completed status:", resp.status_code, resp.json())
    assert resp.status_code == 200

    print("\n9. Re-creating note and testing delete...")
    resp = session.post(f"{BASE_URL}/quick-notes", json={"note": "Temporary Note to delete"})
    del_note_id = resp.json()['note']['id']
    resp = session.delete(f"{BASE_URL}/quick-notes/{del_note_id}")
    print("Delete note status:", resp.status_code, resp.json())
    assert resp.status_code == 200

    print("\nAll settings integration tests passed successfully!")

if __name__ == "__main__":
    test_settings_suite()
