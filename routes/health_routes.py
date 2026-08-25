from flask import Blueprint, jsonify
from config import Config
from services.gemini_service import GeminiService

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health/gemini', methods=['GET'])
def gemini_health():
    """Return Gemini configuration and connectivity status.
    """
    configured = bool(Config.GEMINI_API_KEY)
    connection_status = 'FAIL'
    if configured:
        try:
            # Minimal prompt for quick test
            result = GeminiService.generate_json('{"test": "ping"}', fallback_mock={"test": "mock"})
            connection_status = 'PASS' if result else 'FAIL'
        except Exception:
            connection_status = 'FAIL'
    else:
        connection_status = 'NOT_CONFIGURED'

    return jsonify({
        "Gemini": {
            "Configured": "✓" if configured else "✗",
            "Connection": connection_status
        }
    })
