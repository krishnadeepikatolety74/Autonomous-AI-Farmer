"""
Recommendation service — high-level helpers for creating,
fetching and summarizing recommendations.
"""
from models.recommendation_model import RecommendationModel


class RecommendationService:
    @staticmethod
    def get_active_summary(farm_id):
        """Return counts by priority for dashboard cards."""
        recs = RecommendationModel.get_active(farm_id)
        summary = {"high": 0, "medium": 0, "low": 0, "total": len(recs)}
        for r in recs:
            p = (r.get("priority") or "Low").lower()
            if p in summary:
                summary[p] += 1
        return summary

    @staticmethod
    def push_actions(farm_id, agent_name, actions):
        """Upsert: clear pending from agent then insert new actions list."""
        RecommendationModel.clear_active_by_agent(farm_id, agent_name)
        for act in actions:
            RecommendationModel.create(
                farm_id=farm_id,
                agent_name=agent_name,
                title=act.get("title", "Action Required"),
                description=act.get("description", ""),
                priority=act.get("priority", "Medium"),
            )

    @staticmethod
    def translate_active_recommendations(farm_id, target_lang_code):
        """Translate all active recommendations for a farm into target language code."""
        from models.recommendation_model import RecommendationModel
        from services.gemini_service import GeminiService
        from services.language_service import LanguageService
        import json

        target_lang = LanguageService.get_language_name(target_lang_code)
        
        recs = RecommendationModel.get_active(farm_id)
        if not recs:
            return

        items_to_translate = []
        for r in recs:
            items_to_translate.append({
                "id": r["id"],
                "title": r["title"],
                "description": r["description"]
            })

        prompt = (
            f"You are a professional agricultural translator. "
            f"Please translate the following recommendation list into {target_lang}. "
            f"You MUST keep the IDs intact and only translate the 'title' and 'description' fields.\n\n"
            f"Recommendations:\n{json.dumps(items_to_translate, ensure_ascii=False)}\n\n"
            f"Output a strict JSON array matching the input structure: "
            f"[ {{\"id\": id, \"title\": \"translated title\", \"description\": \"translated description\"}} ]"
        )

        try:
            translations = GeminiService.generate_json(
                prompt=prompt,
                system_instruction=f"You are an expert translator. Translate titles and descriptions of agricultural recommendations into {target_lang}.",
                fallback_mock=[],
                lang_code=target_lang_code
            )
            
            if isinstance(translations, list):
                for item in translations:
                    rec_id = item.get("id")
                    title = item.get("title")
                    desc = item.get("description")
                    if rec_id and title and desc:
                        RecommendationModel.update_texts(rec_id, title, desc)
        except Exception as e:
            # Avoid printing directly to console to prevent encoding issues, log silently or print repr
            pass
