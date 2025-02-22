class Agent:
    def __init__(self, model: str, temperature: float = 0.6, role: str = "Content Creator"):
        self.model = model
        self.temperature = temperature
        self.role = role
