from flask import Blueprint, request, jsonify, g, session, current_app, Response
from utils.auth import login_required
from models import FarmModel, AgentChatModel, UserModel
from services.agent_chat_service import AgentChatService
from services.elevenlabs_service import ElevenLabsService

agent_chat_bp = Blueprint('agent_chat', __name__)

SLUG_MAP = {
    'weather': 'Weather Agent',
    'soil': 'Soil Agent',
    'crop-disease': 'Crop Disease Agent',
    'irrigation': 'Irrigation Agent',
    'fertilizer': 'Fertilizer Agent',
    'market': 'Market Agent',
    'farm-planning': 'Farm Planning Agent'
}

@agent_chat_bp.route('/api/agent-chat', methods=['POST'])
@login_required
def chat():
    """Submit a query message to a specific agent."""
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

    agent_slug = data.get('agent', '')
    if agent_slug not in SLUG_MAP:
        return jsonify({
            "success": False,
            "message": "Invalid or missing agent identifier.",
            "error_code": "INVALID_AGENT"
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

    try:
        reply = AgentChatService.generate_reply(user_id, agent_slug, message, language)
        
        audio_available = False
        from config import Config
        if Config.ELEVENLABS_API_KEY:
            # te, ta, kn use client-side TTS fallback, so we mark it as audio_available = False or True
            # Wait, ElevenLabs is available for hi and en.
            # Let's see if is_language_supported checks standard models
            if ElevenLabsService.is_language_supported(language) and language not in {'te', 'ta', 'kn'}:
                audio_available = True

        return jsonify({
            "success": True,
            "role": "assistant",
            "agent": agent_slug,
            "message": reply,
            "language": language,
            "audio_available": audio_available
        })
    except Exception as e:
        current_app.logger.error(f"Agent Chatbot error: {e}")
        return jsonify({
            "success": False,
            "message": "AI service is temporarily unavailable. Please try again.",
            "error_code": "CHAT_PROCESSING_ERROR"
        }), 500


@agent_chat_bp.route('/api/agent-chat/history', methods=['GET'])
@login_required
def history():
    """Fetch recent chat logs for the specific agent/farm context."""
    user = g.user
    agent_slug = request.args.get('agent', '')
    if agent_slug not in SLUG_MAP:
        return jsonify({"error": "Invalid or missing agent identifier."}), 400

    agent_name = SLUG_MAP[agent_slug]
    farm = FarmModel.get_by_user_id(user['id'])
    farm_id = farm['id'] if farm else None
    
    limit = request.args.get('limit', 20, type=int)
    if limit > 100:
        limit = 100

    try:
        msgs = AgentChatModel.get_history(user['id'], farm_id, agent_name, limit)
        return jsonify({
            "success": True,
            "history": msgs
        })
    except Exception as e:
        return jsonify({"error": f"Error fetching message history: {str(e)}"}), 500


@agent_chat_bp.route('/api/agent-chat/clear', methods=['POST'])
@login_required
def clear():
    """Wipe out chat history log for the specific agent/farm context."""
    user = g.user
    data = request.get_json(silent=True) or {}
    agent_slug = data.get('agent', '')
    if agent_slug not in SLUG_MAP:
        return jsonify({"error": "Invalid or missing agent identifier."}), 400

    agent_name = SLUG_MAP[agent_slug]
    farm = FarmModel.get_by_user_id(user['id'])
    farm_id = farm['id'] if farm else None

    try:
        AgentChatModel.clear_history(user['id'], farm_id, agent_name)
        return jsonify({
            "success": True,
            "message": f"Chat history for {agent_name} cleared successfully."
        })
    except Exception as e:
        return jsonify({"error": f"Error clearing message logs: {str(e)}"}), 500


@agent_chat_bp.route('/api/agent-chat/tts', methods=['POST'])
@login_required
def tts():
    """Convert agent text response to voice audio stream using ElevenLabs."""
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
    SUPPORTED_LANGUAGES = {'en', 'te', 'hi', 'ta', 'kn'}
    if language not in SUPPORTED_LANGUAGES:
        language = 'en'

    # Indian regional languages use browser Web Speech API (client-side) because ElevenLabs lacks default voices for te/ta/kn.
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
