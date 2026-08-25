class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def run(self, farm, crop, observation, previous_results=None, memory_context=None):
        """
        Execute the agent's logic. Should be overridden by subclasses.
        Returns a dict of structured results.
        """
        raise NotImplementedError("Each agent must implement its own run logic.")
