from flask import Blueprint, request, jsonify, g, session, current_app, Response
from utils.auth import login_required
from models import FarmModel, ChatModel, UserModel
from services.chatbot_service import ChatbotService
from services.elevenlabs_service import ElevenLabsService

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """Submit a query message to KisanMitra AI."""
    user = g.user
    if not isinstance(user, dict):
        user = {}

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid request payload format.",
            "error_code": "INVALID_PAYLOAD"
        }), 400

    message = data.get('message', '')
    if message is None:
        message = ''
    else:
        message = str(message).strip()

    if not message:
        return jsonify({
            "success": False,
            "message": "Message content is required.",
            "error_code": "INVALID_MESSAGE"
        }), 400

    if len(message) > 1000:
        return jsonify({
            "success": False,
            "message": "Message exceeds maximum allowed length of 1000 characters.",
            "error_code": "MESSAGE_TOO_LONG"
        }), 400

    user_id = user.get('id')
    if not user_id:
        return jsonify({
            "success": False,
            "message": "User session is invalid or expired.",
            "error_code": "UNAUTHORIZED"
        }), 401

    language = data.get('language') or session.get('language') or user.get('language') or 'en'
    SUPPORTED_LANGUAGES = {'en', 'te', 'hi', 'ta', 'kn', 'ja', 'ko'}
    if language not in SUPPORTED_LANGUAGES:
        language = 'en'

    # Call service to persist and get reply
    try:
        reply = ChatbotService.generate_reply(user_id, message, language)
        
        audio_available = False
        from config import Config
        if Config.ELEVENLABS_API_KEY:
            from services.elevenlabs_service import ElevenLabsService
            if ElevenLabsService.is_language_supported(language):
                audio_available = True

        return jsonify({
            "success": True,
            "role": "assistant",
            "message": reply,
            "language": language,
            "audio_available": audio_available
        })
    except Exception as e:
        current_app.logger.error(f"Chatbot error: {e}")
        return jsonify({
            "success": False,
            "message": "I couldn't process that request right now.",
            "error_code": "CHAT_PROCESSING_ERROR"
        }), 500


@chatbot_bp.route('/api/chat/history', methods=['GET'])
@login_required
def history():
    """Fetch recent chat logs for user/farm context."""
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    farm_id = farm['id'] if farm else None
    
    limit = request.args.get('limit', 20, type=int)
    if limit > 100:
        limit = 100

    try:
        msgs = ChatModel.get_history(user['id'], farm_id, limit)
        return jsonify({
            "success": True,
            "history": msgs
        })
    except Exception as e:
        return jsonify({"error": f"Error fetching message history: {str(e)}"}), 500


@chatbot_bp.route('/api/chat/clear', methods=['POST'])
@login_required
def clear():
    """Wipe out chat history log."""
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    farm_id = farm['id'] if farm else None

    try:
        ChatModel.clear_history(user['id'], farm_id)
        return jsonify({
            "success": True,
            "message": "Chat history cleared successfully."
        })
    except Exception as e:
        return jsonify({"error": f"Error clearing message logs: {str(e)}"}), 500


@chatbot_bp.route('/api/chat/status', methods=['GET'])
@login_required
def status():
    """Verify backend settings for AI services and Ngrok info."""
    from config import Config
    user = UserModel.find_by_id(g.user['id'])
    
    status_info = {
        "gemini_configured": bool(Config.GEMINI_API_KEY),
        "ngrok_enabled": Config.CHATBOT_NGROK_ENABLED,
        "ngrok_url": Config.NGROK_URL if Config.CHATBOT_NGROK_ENABLED else "",
        "elevenlabs_configured": bool(Config.ELEVENLABS_API_KEY),
        "voice_responses": bool(user.get('voice_responses', 1)) if user else True,
        "auto_play_voice": bool(user.get('auto_play_voice', 0)) if user else False,
        "voice": user.get('voice', 'Default') if user else 'Default'
    }
    return jsonify(status_info)


@chatbot_bp.route('/api/chat/tts', methods=['POST'])
@login_required
def tts():
    """Convert KisanMitra text response to voice audio stream."""
    user = g.user
    if not isinstance(user, dict):
        user = {}

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request payload format."}), 400

    text = data.get('text', '')
    if text is None:
        text = ''
    else:
        text = str(text).strip()

    if not text:
        return jsonify({"error": "Text payload is required."}), 400

    language = data.get('language') or session.get('language') or user.get('language') or 'en'
    SUPPORTED_LANGUAGES = {'en', 'te', 'hi', 'ta', 'kn', 'ja', 'ko'}
    if language not in SUPPORTED_LANGUAGES:
        language = 'en'

    # Indian regional languages use browser Web Speech API (client-side).
    # ElevenLabs does not reliably support te/ta/kn without a specialised voice clone.
    BROWSER_ONLY_LANGS = {'te', 'ta', 'kn'}
    if language in BROWSER_ONLY_LANGS:
        return jsonify({"error": "browser_tts_only", "message": "Use client-side TTS for this language."}), 404

    # Explicit check if model supports this language
    if not ElevenLabsService.is_language_supported(language):
        return jsonify({"error": "Voice playback is unavailable for this language."}), 400

    try:
        audio_data = ElevenLabsService.text_to_speech(text, language=language)
        if audio_data:
            return Response(audio_data, mimetype="audio/mpeg")
        else:
            return jsonify({"error": "ElevenLabs configuration missing or API call failed. Using client-side TTS fallback."}), 404
    except Exception as e:
        current_app.logger.error(f"TTS error: {e}")
        return jsonify({"error": "ElevenLabs invocation failed."}), 500


@chatbot_bp.route('/kisanmitra')
@login_required
def chat_page():
    """Render the dedicated full-pane KisanMitra AI chatbot dashboard page."""
    from flask import render_template
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    return render_template('chatbot.html', user=user, farm=farm)
