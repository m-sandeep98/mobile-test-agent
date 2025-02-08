import json
import time
from slugify import slugify
from clients.openai_client import OpenAIClient
from clients.showui_client import ShowUiClient
from controllers.device_controller import DeviceController
from utils.action_logger import ActionLogger
from utils.step_manager import StepManager
from utils.util import validate_openai_json
from handlers.action_handler import ActionHandler
from .system_prompt import system_prompt

class TestController:
    """
    Orchestrates the entire flow:
      - capturing screenshots
      - calling OpenAI for step suggestions
      - calling ShowUI for coordinates
      - asking user for approval
      - executing device actions
      - logging actions
    """

    def __init__(
        self,
        openai_client: OpenAIClient,
        showui: ShowUiClient,
        device: DeviceController,
        step_manager: StepManager
    ):
        self.openai_client = openai_client
        self.showui = showui
        self.device = device
        self.step_manager = step_manager

    def run_test(self, test_goal: str):
        """
        Runs an interactive test session given a single test goal (e.g. "Test the search bar").
        """
        # Take initial screenshot
        logger = ActionLogger(log_file_path=f"{slugify(test_goal)[:20]}.txt")
        action_data_logger= ActionLogger(log_file_path=f"{slugify(test_goal)[:20]}_action.json")
        action_handler = ActionHandler(self.device, self.showui, logger, action_data_logger, self.step_manager)

        while True:

            timestamp = int(time.time())

            screenshot_path = f"screenshots/screenshot_{timestamp}.png"

            self.device.take_screenshot(screenshot_path)

            user_prompt = f"Goal: {test_goal}"

            next_step_str = self.openai_client.get_next_step(
                screenshot_path=screenshot_path,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                previous_steps=self.step_manager.get_steps_as_text(),
                user_feedback=self.step_manager.get_user_feedback()
            )
            validate_openai_json(next_step_str)
            print(f"\n[OpenAI Suggestion]: {next_step_str}")

            user_input = input("Approve this step? (yes/no/quit): ").strip().lower()
            if user_input == "quit":
                print("[TestController] User ended the test session.")
                break
            elif user_input == "no":
                self.step_manager.add_user_feedback(next_step_str, False)
                print("[TestController] Skipping this step.")
                continue
            elif user_input == "yes":
                self.step_manager.add_user_feedback(next_step_str, True)
                try:
                    action_data = json.loads(next_step_str)
                except json.JSONDecodeError:
                    print("[TestController] Could not parse JSON. Skipping.")
                    continue
                if action_data.get("action", "").lower() == "terminate":
                    break
                action_handler.handle_action(action_data, screenshot_path)
            else:
                print("[TestController] Invalid input. Please answer yes/no/quit.")

        print("[TestController] Test session ended.")
