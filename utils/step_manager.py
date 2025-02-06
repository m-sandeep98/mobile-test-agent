class StepManager:
    def __init__(self):
        self.steps = []

    def add_step(self, step: str):
        self.steps.append(step)

    def get_steps_as_text(self) -> str:
        return "\n".join(self.steps)