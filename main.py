import os
from utils.step_manager import StepManager
from controllers.test_controller import TestController
from clients.openai_client import OpenAIClient
from clients.showui_client import ShowUiClient
from controllers.device_controller import DeviceController
from utils.action_logger import ActionLogger

def main():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    openai_client = OpenAIClient(
        api_key=OPENAI_API_KEY,
        model_name="gpt-4o" 
    )
    showui_client = ShowUiClient()
    device_ctrl = DeviceController(
        appium_server="http://127.0.0.1:4723",
        desired_caps={
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "automationName": "UiAutomator2",
            "noReset": True,
            "newCommandTimeout": 600
        }
    )
    step_manager = StepManager()

    test_controller = TestController(
        openai_client=openai_client,
        showui=showui_client,
        device=device_ctrl,
        step_manager=step_manager
    )

    # Get the user's test goal
    test_goal = input("Enter your test goal: ").strip()
    if not test_goal:
        print("No test goal provided. Exiting.")
        return

    # Start the interactive session
    test_controller.run_test(test_goal)
    print("\nDone. All actions are logged in test_script.txt.")

if __name__ == "__main__":
    main()
