from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time
import hashlib

class DeviceController:
    def __init__(self, appium_server: str, desired_caps: dict):
        self.driver = webdriver.Remote(appium_server, options=UiAutomator2Options().load_capabilities(desired_caps))

    def tap(self, x: float, y: float):
        try:
            self.driver.tap([(x, y)], 100)
            self._wait_for_screen_to_settle()
        except Exception as e:
            print(f"[DeviceController] Failed to tap at ({x},{y}): {e}")

    def type_text(self, text: str):
        try:
            focused_element = self.driver.find_element(
                by=AppiumBy.XPATH,
                value='//*[@focused="true"]'
            )
            focused_element.send_keys(text)
        except Exception as e:
            print(f"[DeviceController] Could not type text")

    def scroll(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """
        Scrolls starting from (start_x, start_y) in the given direction.
        """
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration=800)
            self._wait_for_screen_to_settle()
            print(f"[DeviceController] Scrolled ({start_x}, {start_y}) to {end_x}, {end_y}")
        except Exception as e:
            print(f"[DeviceController] Scroll failed")


    def take_screenshot(self, file_path: str):
        self.driver.save_screenshot(file_path)

    def terminate_app(self, package_name: str):
        self.driver.terminate_app(package_name)
    
    def _wait_for_screen_to_settle(self, timeout=10, interval=0.5):
        """
        Waits until the screen stops changing, based on consecutive screenshot hashes.
        :param timeout: Max time (seconds) to wait before giving up.
        :param interval: How often to capture screenshots.
        :return: True if stabilized, False if timed out.
        """
        start_time = time.time()
        prev_hash = None

        while time.time() - start_time < timeout:
            image_data = self.driver.get_screenshot_as_png()
            current_hash = hashlib.md5(image_data).hexdigest()

            if prev_hash == current_hash:
                return True

            prev_hash = current_hash
            time.sleep(interval)

        return False
