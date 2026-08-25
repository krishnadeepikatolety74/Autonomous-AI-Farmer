"""
Memory service — helpers to build the textual memory context string
that agents receive to understand historical farm state.
"""
import json
from models.memory_model import MemoryModel


class MemoryService:
    @staticmethod
    def get_context_string(farm_id, limit=3):
        """Return a compact string of recent farm memory for agent prompts."""
        memories = MemoryModel.get_recent(farm_id, limit=limit)
        if not memories:
            return "No previous farm history available."
        parts = []
        for m in memories:
            parts.append(
                f"[{m.get('created_at', 'unknown date')}] "
                f"{m.get('plan_summary', '')} — "
                f"{m.get('risk_assessment', '')}"
            )
        return "\n".join(parts)

    @staticmethod
    def save_plan(farm_id, summary, risk_assessment):
        """Persist a new memory snapshot."""
        MemoryModel.add(farm_id, summary, risk_assessment)
