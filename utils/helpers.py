import os
import json
import datetime
from flask import g, current_app

def get_translation(key, default=None):
    """Load translation key based on active user context language."""
    lang = 'en'
    if hasattr(g, 'user') and g.user and g.user.get('language'):
        lang = g.user['language']
        
    translations_path = os.path.join(current_app.config['TRANSLATIONS_DIR'], f"{lang}.json")
    if not os.path.exists(translations_path):
        translations_path = os.path.join(current_app.config['TRANSLATIONS_DIR'], 'en.json')
        
    try:
        with open(translations_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, default or key)
    except Exception as e:
        print(f"Error loading translation dict: {e}")
        return default or key

def _safe_date(value):
    """Safely convert a datetime object OR a string to a date-only string (YYYY-MM-DD).
    Fixes: 'datetime.datetime object has no attribute split'.
    """
    if value is None:
        return ''
    # Real datetime / date objects — format directly, no .split() needed
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.strftime('%Y-%m-%d')
    # String fallback — strip microseconds fraction then time portion
    s = str(value)
    return s.split('.')[0].split(' ')[0]

def register_template_helpers(app):
    """Inject helpers directly to Jinja2 context variables."""
    # Register as a Jinja2 filter: {{ value|safe_date }}
    app.jinja_env.filters['safe_date'] = _safe_date

    @app.context_processor
    def utility_processor():
        return dict(
            t=get_translation,
            format_date=_safe_date,
            user=g.user if hasattr(g, 'user') else None
        )

