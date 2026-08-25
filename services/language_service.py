class LanguageService:
    LANG_MAP = {
        'en': 'English',
        'te': 'Telugu',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'kn': 'Kannada',
        'ja': 'Japanese',
        'ko': 'Korean'
    }

    @classmethod
    def get_language_name(cls, code):
        """Translate language code to language name."""
        return cls.LANG_MAP.get(code, 'English')

    @classmethod
    def get_supported_codes(cls):
        """Return list of supported language codes."""
        return list(cls.LANG_MAP.keys())

    @classmethod
    def get_language_directive(cls, code):
        """Get the specific prompt instruction for the selected language."""
        lang_name = cls.get_language_name(code)
        return f"Respond entirely in natural {lang_name}. Use terminology that is understandable to farmers. Do not mix languages."
