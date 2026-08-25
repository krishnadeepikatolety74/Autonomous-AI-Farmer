from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
from services.elevenlabs_service import ElevenLabsService

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/api/tts', methods=['POST'])
def generate_tts():
    """Generate speech audio from text using ElevenLabs API.
    Expects JSON payload: {"text": "...", "voice_id": "optional"}
    Returns: audio/mpeg file or error JSON.
    """
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    voice_id = data.get('voice_id')
    language = data.get('language') or 'en'
    if not text:
        return jsonify({"error": "'text' field is required"}), 400

    # Verify model compatibility with language
    if not ElevenLabsService.is_language_supported(language):
        return jsonify({"error": "Voice playback is unavailable for this language."}), 400

    audio_bytes = ElevenLabsService.text_to_speech(text, voice_id, language=language)
    if not audio_bytes:
        return jsonify({"error": "Text-to-speech generation failed"}), 500
    # Return audio as streaming response
    return send_file(
        BytesIO(audio_bytes),
        mimetype='audio/mpeg',
        as_attachment=False,
        download_name='speech.mp3'
    )
