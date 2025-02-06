class ActionLogger:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        with open(self.log_file_path, 'w') as f:
            pass

    def log_action(self, action: str):
        with open(self.log_file_path, 'a') as f:
            f.write(f"{action}\n")