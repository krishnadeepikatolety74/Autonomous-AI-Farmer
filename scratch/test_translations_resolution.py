import json
import os

TRANSLATIONS_DIR = r"c:\Users\kooki\Desktop\Farm\translations"
LANGUAGES = ["en", "te", "hi", "ta", "kn", "ja", "ko"]

print("=== Checking Translation Files JSON Validity ===")
for lang in LANGUAGES:
    file_path = os.path.join(TRANSLATIONS_DIR, f"{lang}.json")
    if not os.path.exists(file_path):
        print(f"[MISSING] translation file: {file_path}")
        continue
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Spot check keys
            expected_keys = ["settings_title", "profile_section", "language_system", "btn_save"]
            missing_keys = [k for k in expected_keys if k not in data]
            if missing_keys:
                print(f"[WARN] {lang}.json is missing keys: {missing_keys}")
            else:
                print(f"[OK] {lang}.json loaded successfully. Total keys: {len(data)}")
    except Exception as e:
        print(f"[ERROR] Error loading {lang}.json: {e}")

print("=== Done ===")
