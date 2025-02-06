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
        timestamp = int(time.time())
        screenshot_path = f"screenshots/screenshot_{timestamp}.png"
        self.device.take_screenshot(screenshot_path)
        logger = ActionLogger(log_file_path=f"{slugify(test_goal)}.txt")
        action_data_logger= ActionLogger(log_file_path=f"{slugify(test_goal)}_action.json")
        action_handler = ActionHandler(self.device, self.showui, logger, action_data_logger, self.step_manager)

        while True:
            previous_steps_text = self.step_manager.get_steps_as_text()

            system_prompt = (
                "You are a mobile testing AI. "
                "You must ONLY output valid JSON in the format:\n"
                "{\"action\":\"<click|scroll|type>\",\"desc\":\"<3-4 words>\"}.\n"
                "No code fences or markdown.No extra text.\n"
                "Supported actions: click, scroll, type.\n"
                "desc must be 1-4 letters max. Can contain any atrtibute like color, type etc.\n"
                "For scroll, desc should be 'up', 'down', 'left', or 'right', and a new json key 'start_from' should specify the exact element desc of the scroll start position.\n"
                "In cases of type, the desc should be a mock value based on the field.\n"
            )
            user_prompt = f"Goal: {test_goal}"

            next_step_str = self.openai_client.get_next_step(
                screenshot_path=screenshot_path,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                previous_steps=previous_steps_text
            )
            validate_openai_json(next_step_str)
            print(f"\n[OpenAI Suggestion]: {next_step_str}")

            user_input = input("Approve this step? (yes/no/quit): ").strip().lower()
            if user_input == "quit":
                print("[TestController] User ended the test session.")
                break
            elif user_input == "no":
                print("[TestController] Skipping this step.")
                continue
            elif user_input == "yes":

                try:
                    action_data = json.loads(next_step_str)
                except json.JSONDecodeError:
                    print("[TestController] Could not parse JSON. Skipping.")
                    continue

                action_handler.handle_action(action_data, screenshot_path)

                self.device.take_screenshot(screenshot_path)
            else:
                print("[TestController] Invalid input. Please answer yes/no/quit.")

        print("[TestController] Test session ended.")
