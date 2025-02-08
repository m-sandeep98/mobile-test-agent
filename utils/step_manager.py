class StepManager:
    def __init__(self):
        self.steps = []
        self.user_feedback = []  

    def add_step(self, step: str):
        self.steps.append(step)

    def get_steps_as_text(self) -> str:
        return "\n".join(self.steps)
    
    def get_steps_as_text(self) -> str:
        return "\n".join(self.steps)

    def add_user_feedback(self, action: str, approved: bool):
        feedback = f"{'Accepted' if approved else 'Rejected'}: {action}"
        self.user_feedback.append(feedback)

    def get_user_feedback(self) -> str:
        return "\n".join(self.user_feedback)