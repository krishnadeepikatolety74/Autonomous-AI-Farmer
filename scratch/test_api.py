import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import io, json
from PIL import Image

# Create a test image simulating a diseased leaf
img = Image.new('RGB', (200, 200), color=(60, 120, 40))
buf = io.BytesIO()
img.save(buf, format='JPEG')
img_bytes = buf.getvalue()

from app import create_app
app = create_app()

with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['user_id'] = 1

    data = {
        'image': (io.BytesIO(img_bytes), 'test_leaf.jpg', 'image/jpeg'),
        'language': 'en'
    }
    resp = c.post('/api/crop-analysis',
                  data=data,
                  content_type='multipart/form-data',
                  headers={'X-Requested-With': 'XMLHttpRequest'})
    
    status = resp.status_code
    result = json.loads(resp.data)
    print(f"HTTP Status: {status}")
    success = result.get("success")
    print(f"Success: {success}")
    if success:
        analysis = result.get("analysis", {})
        print(f"Crop: {analysis.get('crop','?')}")
        print(f"Detected Issue: {analysis.get('detected_issue','?')}")
        print(f"Severity: {analysis.get('severity','?')}")
        print(f"Confidence: {analysis.get('confidence','?')}")
        symptoms = analysis.get('visual_symptoms', [])
        print(f"Symptoms count: {len(symptoms)}")
        print(f"img_src: {result.get('img_src','?')}")
        print("TEST RESULT: PASS")
    else:
        err = result.get("error")
        print(f"Error: {err}")
        print("TEST RESULT: FAIL")
