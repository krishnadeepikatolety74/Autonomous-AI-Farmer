import os
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*urllib3.*')
warnings.filterwarnings('ignore', message='.*charset_normalizer.*')
from flask import Flask, render_template, g
from config import Config
import database
from utils.auth import load_logged_in_user
from utils.helpers import register_template_helpers

# Blueprints
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.farm_routes import farm_bp
from routes.agent_routes import agent_bp
from routes.recommendation_routes import recommendation_bp
from routes.memory_routes import memory_bp
from routes.settings_routes import settings_bp
from routes.chatbot_routes import chatbot_bp
from routes.alert_routes import alert_bp
from routes.calendar_routes import calendar_bp
from routes.report_routes import report_bp
from routes.health_routes import health_bp
from routes.tts_routes import tts_bp
from routes.agent_chat_routes import agent_chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Upload folder configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize Database hooks
    database.init_app(app)

    # Register Helpers
    register_template_helpers(app)

    # Register Request Middleware Hooks
    @app.before_request
    def before_request_hook():
        load_logged_in_user()

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(farm_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(memory_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(tts_bp)
    app.register_blueprint(agent_chat_bp)



    # Public Routes
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/health')
    def health():
        return {"status": "healthy"}

    # Initialize DB file on launch if not exists
    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            print("Initializing database file...")
            database.init_db()

        # ElevenLabs discovery runs only when an API key is configured
        try:
            from services.elevenlabs_service import ElevenLabsService
            from config import Config as _Cfg
            _key = getattr(_Cfg, 'ELEVENLABS_API_KEY', None)
            if _key and len(_key) > 30 and not _key.startswith('gsk_'):
                res = ElevenLabsService.discover_and_update_env()
                if res.get('success'):
                    print(f"ElevenLabs discovery successful! Updates: {res['updates']}")
        except Exception:
            pass

    return app

# Application entry point
app = create_app()

if __name__ == '__main__':
    # Run dev server locally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
