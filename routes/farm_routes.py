import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify, session
from utils.auth import login_required
from utils.validators import validate_observation_input
from models import FarmModel, CropModel, ObservationModel, FarmFertilizerModel, FERTILIZER_LIST
from services.weather_service import WeatherService

farm_bp = Blueprint('farm', __name__)

@farm_bp.route('/farm', methods=['GET', 'POST'])
@login_required
def farm():
    user = g.user
    
    if request.method == 'POST':
        # Save farm profile
        farm_name = request.form.get('farm_name', '').strip()
        location = request.form.get('location', '').strip()
        area = request.form.get('area', '0')
        soil_type = request.form.get('soil_type', '').strip()
        irrigation_method = request.form.get('irrigation_method', '').strip()

        if not farm_name or not location:
            flash('Farm name and location are required.', 'error')
        else:
            try:
                area = float(area)
            except ValueError:
                area = 0.0
                
            FarmModel.create_or_update(user['id'], farm_name, location, area, soil_type, irrigation_method)

            # Save crop info if provided
            crop_name = request.form.get('crop_name', '').strip()
            variety = request.form.get('variety', '').strip()
            planting_date = request.form.get('planting_date', '').strip()
            stage = request.form.get('stage', '').strip()

            farm_data = FarmModel.get_by_user_id(user['id'])
            if crop_name and farm_data:
                CropModel.create_or_update(farm_data['id'], crop_name, variety, planting_date, stage)

            flash('Farm profile saved successfully!', 'success')
            return redirect(url_for('farm.farm'))

    farm_data = FarmModel.get_by_user_id(user['id'])
    crop_data = CropModel.get_by_farm_id(farm_data['id']) if farm_data else None
    observations = ObservationModel.get_all(farm_data['id'], limit=10) if farm_data else []
    fertilizer_data = FarmFertilizerModel.get(farm_data['id']) if farm_data else {'fertilizers': {}, 'notes': ''}

    return render_template('farm.html',
        user=user,
        farm=farm_data,
        crop=crop_data,
        observations=observations,
        fertilizer_data=fertilizer_data,
        fertilizer_list=FERTILIZER_LIST
    )

@farm_bp.route('/farm/observation', methods=['POST'])
@login_required
def add_observation():
    user = g.user
    farm_data = FarmModel.get_by_user_id(user['id'])
    
    if not farm_data:
        flash('Please set up your farm profile first.', 'error')
        return redirect(url_for('farm.farm'))

    # Validate observation fields
    valid, error_msg = validate_observation_input(request.form)
    if not valid:
        flash(error_msg, 'error')
        return redirect(url_for('farm.farm'))

    ObservationModel.add(
        farm_id=farm_data['id'],
        soil_moisture=float(request.form.get('soil_moisture', 0)),
        soil_ph=float(request.form.get('soil_ph', 7)),
        nitrogen=float(request.form.get('nitrogen', 0)),
        phosphorus=float(request.form.get('phosphorus', 0)),
        potassium=float(request.form.get('potassium', 0)),
        temperature=float(request.form.get('temperature', 0)),
        humidity=float(request.form.get('humidity', 0)),
        rainfall=float(request.form.get('rainfall', 0)),
        crop_health=float(request.form.get('crop_health', 100)),
        disease_notes=request.form.get('disease_notes', ''),
        market_price=float(request.form.get('market_price', 0))
    )

    flash('Observation recorded successfully!', 'success')
    return redirect(url_for('farm.farm'))


@farm_bp.route('/farm/fertilizers', methods=['POST'])
@login_required
def save_fertilizers():
    """Save the farmer's current fertilizer usage."""
    user = g.user
    farm_data = FarmModel.get_by_user_id(user['id'])

    if not farm_data:
        flash('Please set up your farm profile first.', 'error')
        return redirect(url_for('farm.farm'))

    # Collect checked fertilizers + their doses and units
    fertilizer_usage = {}
    for fert in FERTILIZER_LIST:
        # Checkbox key
        fkey = 'fert_' + fert.replace(' ', '_').replace('/', '_')
        dose_key = 'dose_' + fert.replace(' ', '_').replace('/', '_')
        unit_key = 'unit_' + fert.replace(' ', '_').replace('/', '_')
        if request.form.get(fkey):
            # Parse numeric value
            try:
                val = float(request.form.get(dose_key, 0) or 0)
            except ValueError:
                val = 0.0
            unit = request.form.get(unit_key, 'kg')
            fertilizer_usage[fert] = {'value': val, 'unit': unit}

    notes = request.form.get('fertilizer_notes', '').strip()
    FarmFertilizerModel.save(farm_data['id'], fertilizer_usage, notes)
    flash('Fertilizer usage saved successfully!', 'success')
    return redirect(url_for('farm.farm'))

@farm_bp.route('/crop-analysis', methods=['GET', 'POST'])
@login_required
def crop_analysis():
    user = g.user
    farm_data = FarmModel.get_by_user_id(user['id'])
    
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image file selected.', 'error')
            return redirect(url_for('farm.crop_analysis'))
            
        file = request.files['image']
        if file.filename == '':
            flash('No image file selected.', 'error')
            return redirect(url_for('farm.crop_analysis'))

        # Read file data as bytes
        import io
        import base64
        import json
        import re
        from services.gemini_service import GeminiService

        allowed_extensions = {'png', 'jpg', 'jpeg'}
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in allowed_extensions:
            flash('Unsupported file format. Please upload JPG, JPEG, or PNG.', 'error')
            return redirect(url_for('farm.crop_analysis'))

        try:
            image_bytes = file.read()
            mime_type = f"image/{ext}" if ext != 'jpg' else 'image/jpeg'

            # Convert to base64 for embedding in the HTML response
            encoded_img = base64.b64encode(image_bytes).decode('utf-8')
            img_src = f"data:{mime_type};base64,{encoded_img}"

            # Gemini Prompt
            prompt = """
You are an expert Agricultural AI performing visual crop health analysis.

Analyze the uploaded image carefully and provide a structured assessment.

STEP 1 — Check image validity:
- If the image does NOT appear to contain a plant, crop, leaf, or any agricultural produce:
  Set error = "The uploaded image does not appear to contain a crop. Please upload a clear crop or leaf image."
- If the image is too blurry, dark, or unclear to analyze reliably:
  Set error = "The image is not clear enough for reliable analysis. Please capture a closer image of the affected crop or leaf."
- If valid, set error = null and proceed.

STEP 2 — If image is valid, identify and analyze:
1. Crop: Identify the likely crop (e.g. Tomato, Rice, Wheat, Maize, Cotton, Chilli, etc.). If unsure, state "Uncertain — possibly [crop name]".
2. Health Status: One of — Healthy / Mild Stress / Moderate Stress / Severe Stress
3. Possible Issue: The most likely visual problem (e.g. Healthy, Leaf Blight, Powdery Mildew, Rust, Root Rot, Insect Damage, Yellowing)
4. Possible Disease: Describe any suspected disease symptoms visible. Use language like "Possible", "Likely", "Suspected". Do not claim certainty.
5. Possible Pest: Describe any visible pest damage indicators (holes, webbing, frass, feeding patterns). Use "Possible pest damage" rather than confirming specific pest.
6. Possible Nutrient Deficiency: Look for visual signs:
   - Yellowing of older leaves = Possible Nitrogen deficiency
   - Purple/reddish underside = Possible Phosphorus deficiency
   - Leaf edge browning/scorching = Possible Potassium deficiency
   - Interveinal chlorosis = Possible Iron/Magnesium deficiency
   State "No visible deficiency signs" if none detected.
7. Severity: High / Medium / Low / None
8. Confidence: Percentage (e.g. 78) — be honest; lower confidence if image is partially unclear.
9. Recommended Action: Practical next step the farmer should take.
10. Prevention: How to prevent this issue from worsening or recurring.
11. Reasoning: Brief explanation of what visual cues led to your assessment.

IMPORTANT RULES:
- Never claim a 100% certain diagnosis — always use "Possible", "Likely", "Suspected", or "AI Detection".
- Do not fabricate diseases if the crop looks healthy.
- If the crop appears healthy, say so clearly and provide maintenance advice.

Return ONLY this exact JSON (no markdown, no text outside the JSON):
{
  "crop": "Identified crop or 'Unknown'",
  "health_status": "Healthy / Mild Stress / Moderate Stress / Severe Stress",
  "possible_issue": "Issue name or 'None detected'",
  "possible_disease": "Suspected disease description or 'No disease symptoms detected'",
  "possible_pest": "Suspected pest damage or 'No visible pest damage'",
  "possible_deficiency": "Suspected nutrient deficiency or 'No visible deficiency signs'",
  "severity": "High / Medium / Low / None",
  "confidence": 85,
  "recommended_action": "Specific practical action the farmer should take",
  "prevention": "Preventive measures or maintenance advice",
  "reasoning": "What visual cues led to this assessment",
  "error": null
}
"""

            user_lang = user.get('language', 'en') or 'en'
            # Request Gemini vision analysis
            raw_res = GeminiService.generate_from_image(image_bytes, mime_type, prompt, lang_code=user_lang)
            
            # Clean and parse JSON
            cleaned_res = raw_res.strip()
            json_match = re.search(r'\{.*\}', cleaned_res, re.DOTALL)
            if json_match:
                cleaned_res = json_match.group(0)

            try:
                analysis = json.loads(cleaned_res)
            except Exception:
                analysis = {
                    "crop": "Unknown",
                    "possible_issue": "Error parsing output",
                    "severity": "None",
                    "confidence": 0,
                    "recommended_action": "AI service temporarily unavailable. Please try again.",
                    "prevention": "N/A",
                    "reasoning": raw_res,
                    "error": None
                }

            # Cache the analysis result and image source in session
            session['last_crop_analysis'] = analysis
            session['last_crop_img_src'] = img_src
            session['last_crop_analysis_lang'] = user_lang

            return render_template('crop_analysis.html',
                user=user, farm=farm_data,
                analysis=analysis, img_src=img_src
            )

        except Exception as e:
            flash(f"Image analysis error: {e}", 'error')
            return redirect(url_for('farm.crop_analysis'))

    # GET request
    analysis = session.get('last_crop_analysis')
    img_src = session.get('last_crop_img_src')
    stored_lang = session.get('last_crop_analysis_lang')
    current_lang = user.get('language', 'en') or 'en'

    if analysis and stored_lang != current_lang and not analysis.get('error'):
        # Translate the cached analysis into the new language using Gemini Text
        from services.gemini_service import GeminiService
        from services.language_service import LanguageService
        target_lang_name = LanguageService.get_language_name(current_lang)
        directive = LanguageService.get_language_directive(current_lang)
        
        translation_prompt = f"""
You are a professional agricultural translator. 
Translate the following crop leaf analysis JSON into {target_lang_name}.

Ensure that:
1. JSON keys (such as "crop", "health_status", "possible_issue", "possible_disease", "possible_pest", "possible_deficiency", "severity", "recommended_action", "prevention", "reasoning", "error") remain exactly the same in English. Do NOT change or translate these keys.
2. The values of these keys are translated naturally into {target_lang_name}.
3. The translation is clear, accurate, and appropriate for farmers.
4. Return ONLY the translated JSON structure.

JSON to translate:
{json.dumps(analysis)}
"""
        try:
            translated_analysis = GeminiService.generate_json(
                prompt=translation_prompt,
                system_instruction=f"You are a professional agricultural translator. {directive}",
                fallback_mock=analysis,
                lang_code=current_lang
            )
            if translated_analysis and isinstance(translated_analysis, dict) and "possible_issue" in translated_analysis:
                analysis = translated_analysis
                session['last_crop_analysis'] = analysis
                session['last_crop_analysis_lang'] = current_lang
        except Exception as e:
            print(f"Failed to translate stored analysis: {e}")

    return render_template('crop_analysis.html', user=user, farm=farm_data, analysis=analysis, img_src=img_src)


@farm_bp.route('/api/weather', methods=['GET'])
def live_weather():
    """
    Return live weather JSON for a given location, lat/lon, logged-in user's farm, or auto-detected IP.
    Used by navbar weather badge, agent detail page, and dashboard weather widget.
    """
    user = getattr(g, 'user', None)
    
    # 1. Check query parameters
    location = request.args.get('location')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    weather = None
    resolved_location = None
    
    if lat and lon:
        try:
            lat_f = float(lat)
            lon_f = float(lon)
            resolved_location = request.args.get('display', 'Detected Location')
            weather = WeatherService.fetch_live_weather_by_coords(lat_f, lon_f, resolved_location)
        except ValueError:
            pass

    if not weather and location:
        weather = WeatherService.fetch_live_weather(location)
        if weather:
            resolved_location = weather['location']

    # 2. Fallback to logged-in user's farm location
    if not weather and user:
        farm = FarmModel.get_by_user_id(user['id'])
        if farm and farm.get('location'):
            location = farm['location']
            weather = WeatherService.fetch_live_weather(location)
            if weather:
                resolved_location = weather['location']

    # 3. Fallback to IP-based geocoding
    if not weather:
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip and ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        geo_ip = WeatherService.geocode_ip(client_ip)
        if geo_ip:
            weather = WeatherService.fetch_live_weather_by_coords(geo_ip['lat'], geo_ip['lon'], geo_ip['display'])
            if weather:
                resolved_location = geo_ip['display']
        
        # 4. If geocoding fails or IP is loopback, default to Hyderabad, India
        if not weather:
            location = "Hyderabad, India"
            weather = WeatherService.fetch_live_weather(location)
            if weather:
                resolved_location = weather['location']

    if weather is None:
        return jsonify({
            "success": False,
            "error": "Could not fetch live weather.",
            "weather": None
        }), 503

    return jsonify({
        "success": True,
        "weather": weather,
        "location_input": location or resolved_location
    })



@farm_bp.route('/api/crop-analysis', methods=['POST'])
@login_required
def api_crop_analysis():
    import uuid
    import re
    import json
    import base64
    import traceback
    from flask import current_app
    from werkzeug.utils import secure_filename
    from services.gemini_service import GeminiService
    from services.language_service import LanguageService

    print("[CropAnalysis] Image received")
    user = g.user
    farm_data = FarmModel.get_by_user_id(user['id'])

    if 'image' not in request.files and 'crop_image' not in request.files:
        print("[CropAnalysis] Image validation failed: No image file in request")
        return jsonify({"success": False, "error": "No image file selected."}), 400

    file = request.files.get('image') or request.files.get('crop_image')
    if not file or file.filename == '':
        print("[CropAnalysis] Image validation failed: Empty filename")
        return jsonify({"success": False, "error": "No image file selected."}), 400

    allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_extensions:
        print(f"[CropAnalysis] Image validation failed: Unsupported format '{ext}'")
        return jsonify({"success": False, "error": "Unsupported file format. Please upload JPG, JPEG, PNG, or WEBP."}), 400

    try:
        image_bytes = file.read()
        if len(image_bytes) == 0:
            return jsonify({"success": False, "error": "The uploaded file appears to be empty."}), 400
        if len(image_bytes) > 5 * 1024 * 1024:
            print("[CropAnalysis] Image validation failed: File too large")
            return jsonify({"success": False, "error": "File too large. Please select an image under 5MB."}), 400

        print(f"[CropAnalysis] Image validation passed — {len(image_bytes)} bytes, type: {ext}")

        # Save image to uploads folder
        filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        with open(upload_path, 'wb') as fh:
            fh.write(image_bytes)

        mime_type = 'image/jpeg' if ext == 'jpg' else f"image/{ext}"
        img_src = f"/static/uploads/{filename}"

        # Get language preference
        user_lang = request.form.get('language') or request.args.get('language') or user.get('language', 'en') or 'en'
        if user_lang not in LanguageService.LANG_MAP:
            user_lang = 'en'
        lang_name = LanguageService.get_language_name(user_lang)

        # Assemble farm context (safe even if farm_data is None)
        crop_data = {}
        observation = {}
        if farm_data:
            try:
                crop_data = CropModel.get_by_farm_id(farm_data['id']) or {}
            except Exception:
                crop_data = {}
            try:
                observation = ObservationModel.get_latest(farm_data['id']) or {}
            except Exception:
                observation = {}

        farm_ctx = ""
        if farm_data:
            farm_ctx += f"Farm: {farm_data.get('name','')}, Location: {farm_data.get('location','')}, Soil: {farm_data.get('soil_type','')}, Area: {farm_data.get('area',0)} acres\n"
        if crop_data:
            farm_ctx += f"Crop: {crop_data.get('name','')}, Stage: {crop_data.get('stage','')}, Variety: {crop_data.get('variety','')}\n"
        if observation:
            farm_ctx += (
                f"Soil Moisture: {observation.get('soil_moisture','')}%, pH: {observation.get('soil_ph','')}\n"
                f"N: {observation.get('nitrogen','')} P: {observation.get('phosphorus','')} K: {observation.get('potassium','')} kg/ha\n"
                f"Temp: {observation.get('temperature','')}°C, Humidity: {observation.get('humidity','')}%, Rainfall: {observation.get('rainfall','')}mm\n"
                f"Crop Health: {observation.get('crop_health','')}%, Notes: {observation.get('disease_notes','')}\n"
            )
        if not farm_ctx:
            farm_ctx = "No farm context available. Analyze based on the image alone.\n"

        prompt = f"""You are the Crop Disease Agent of an AI farming system.

Analyze the uploaded crop image carefully.
Identify the crop if possible.
Analyze all visible symptoms in detail.
Determine the most likely disease, disorder, pest damage, nutrient deficiency, or environmental stress visible in the image.

Farm context (use only if relevant):
{farm_ctx}

Answer these 10 questions based on ONLY what is visible in the image:
1. What is visible in the image?
2. What is the likely disease/problem?
3. What caused it?
4. Why may it have happened?
5. What factors may contribute?
6. How severe does it appear?
7. What should the farmer do now?
8. How can the farmer prevent it?
9. What information is missing?
10. How confident is the analysis?

IMPORTANT RULES:
- Do not invent facts not visible in the image.
- If the image is unclear or not a crop/plant, say so explicitly.
- Never claim 100% certainty — always say "Possible", "Likely", or "Suspected".
- Respond entirely in {lang_name}.

Return ONLY this exact JSON structure (no markdown, no explanation outside the JSON):
{{
  "crop": "identified crop name or 'Unknown'",
  "detected_issue": "disease/issue name or 'None detected'",
  "visual_symptoms": [
      "symptom 1",
      "symptom 2"
  ],
  "likely_cause": "description of the most likely cause",
  "contributing_factors": [
      "factor 1",
      "factor 2"
  ],
  "why_it_may_have_occurred": "explanation of why this may have occurred",
  "severity": "Low or Moderate or High or Severe or None",
  "what_to_do_now": [
      "action 1",
      "action 2"
  ],
  "prevention": [
      "prevention measure 1",
      "prevention measure 2"
  ],
  "confidence": "Low or Moderate or High",
  "data_used": [
      "Crop image"
  ],
  "missing_information": [
      "missing info 1"
  ],
  "explanation": "detailed reasoning about what visual cues led to this assessment"
}}

All JSON keys must remain in English exactly as shown. All values must be written in {lang_name}.
"""

        print("[CropAnalysis] Calling Gemini Vision")
        raw_res = GeminiService.generate_from_image(image_bytes, mime_type, prompt, lang_code=user_lang)
        print("[CropAnalysis] Gemini response received")

        # Check for Gemini failure
        if not raw_res or "service temporarily unavailable" in raw_res:
            print("[CropAnalysis] Gemini failed — no valid response returned")
            return jsonify({"success": False, "error": "Image uploaded, but AI analysis could not be completed. Please try again."}), 500

        print(f"[CropAnalysis] Parsing response ({len(raw_res)} chars)")
        cleaned_res = raw_res.strip()

        # Strip markdown code fences if present
        if cleaned_res.startswith("```"):
            cleaned_res = re.sub(r'^```(?:json)?\s*', '', cleaned_res)
            cleaned_res = re.sub(r'\s*```$', '', cleaned_res.rstrip())

        # Extract JSON object
        json_match = re.search(r'\{.*\}', cleaned_res, re.DOTALL)
        if json_match:
            cleaned_res = json_match.group(0)

        try:
            analysis = json.loads(cleaned_res)
            print("[CropAnalysis] JSON parsed successfully")
        except Exception as parse_err:
            print(f"[CropAnalysis] JSON parsing failed: {parse_err}")
            print(f"[CropAnalysis] Raw response was: {raw_res[:500]}")
            # Return structured fallback with the raw text as explanation
            analysis = {
                "crop": "Unknown",
                "detected_issue": "Analysis parsing error",
                "visual_symptoms": [],
                "likely_cause": "Could not parse AI response.",
                "contributing_factors": [],
                "why_it_may_have_occurred": "",
                "severity": "Unknown",
                "what_to_do_now": ["Please try uploading the image again."],
                "prevention": [],
                "confidence": "Low",
                "data_used": ["Crop image"],
                "missing_information": [],
                "explanation": raw_res[:1000] if raw_res else "No response received."
            }

        # Cache analysis result and image source in session for follow-up chat
        session['last_crop_analysis'] = analysis
        session['last_crop_img_src'] = img_src
        session['last_crop_analysis_lang'] = user_lang

        print("[CropAnalysis] Analysis generated successfully")
        print(f"[CropAnalysis] Detected: {analysis.get('detected_issue','?')} | Severity: {analysis.get('severity','?')} | Confidence: {analysis.get('confidence','?')}")
        return jsonify({
            "success": True,
            "analysis": analysis,
            "img_src": img_src
        })

    except Exception as e:
        print(f"[CropAnalysis] EXCEPTION: {e}")
        print(f"[CropAnalysis] TRACEBACK:\n{traceback.format_exc()}")
        return jsonify({"success": False, "error": "Image uploaded, but AI analysis could not be completed. Please try again."}), 500
