import json
class ActionHandler:
    def __init__(self, device, showui, logger, action_data_logger, step_manager):
        self.device = device
        self.showui = showui
        self.logger = logger
        self.action_data_logger = action_data_logger
        self.step_manager = step_manager

        self.action_registry = {
            "click": self.handle_click,
            "type": self.handle_type,
            "scroll": self.handle_scroll,
            "system": self.handle_system
        }

    def handle_action(self, action_data, screenshot_path):
        action = action_data.get("action", "").lower()
        handler = self.action_registry.get(action)

        if handler:
            result = handler(action_data, screenshot_path)
            return result
        else:
            print(f"[ActionHandler] Unknown action: {action}")
            return False

    def handle_click(self, action_data, screenshot_path):
        desc = action_data.get("desc", "")
        (x, y) = self.showui.get_coordinate(screenshot_path, f"click on {desc}")
        if x is not None and y is not None:
            self.device.tap(x, y)
            self.logger.log_action(f"CLICK {desc}")
            self.step_manager.add_step(json.dumps(action_data))
            action_data["coordinates"] = [x, y]
            self.action_data_logger.log_action(json.dumps(action_data))
            return True
        print("[ActionHandler] ShowUI failed to find coordinates.")
        return False

    def handle_type(self, action_data, screenshot_path):
        text_to_type = action_data.get("desc", "")
        try:
            self.device.type_text(text_to_type)
            self.logger.log_action(f"TYPE {text_to_type}")
            self.step_manager.add_step(json.dumps(action_data))
            return True
        except Exception as e:
            print(f"[ActionHandler] Failed to type: {e}")
            return False

    def handle_scroll(self, action_data, screenshot_path):
        direction = action_data.get("desc", "").lower()
        start_from = action_data.get("start_from", "")
        if start_from:
            (start_x, start_y) = self.showui.get_coordinate(screenshot_path, f"Find {start_from}")
            if start_x is not None and start_y is not None:

                window_size = self.device.driver.get_window_size()
                width, height = window_size['width'], window_size['height']

                end_x, end_y = start_x, start_y

                BUFFER_RATIO = 0.3  # 30% buffer from top/bottom
                buffer_pixels = int(height * BUFFER_RATIO)

                if direction == "up":
                    if start_y > (height - buffer_pixels):  # Too close to bottom
                        start_y = height - buffer_pixels
                    end_y = min(height, start_y + (height // 3))
                elif direction == "down":
                    if start_y < buffer_pixels:  # Too close to top
                        start_y = buffer_pixels
                    end_y = max(0, start_y - (height // 3))
                elif direction == "left":
                    end_x = min(width, start_x + (width // 3))
                elif direction == "right":
                    end_x = max(0, start_x - (width // 3))
                else:
                    print(f"[DeviceController] Unknown scroll direction: {direction}")
                    return
                self.device.scroll(start_x, start_y, end_x, end_y)
                self.logger.log_action(f"SCROLL {direction} from {start_from}")
                self.step_manager.add_step(json.dumps(action_data))
                action_data["coordinates"] = [start_x, start_y, end_x, end_y]
                self.action_data_logger.log_action(json.dumps(action_data))
                return True
            print(f"[ActionHandler] ShowUI failed to find coordinates for '{start_from}'.")
        else:
            print(f"[ActionHandler] Missing 'start_from' for scroll action.")
        return False
    
    def handle_system(self, action_data, screenshot_path):
        """
        Handles system actions such as back, home, recent apps, volume control, and power.
        """
        system_action = action_data.get("desc", "").lower()

        system_action_map = {
            "back": 4,  
            "home": 3,  
            "recent_apps": 187,  
            "volume_up": 24,  
            "volume_down": 25, 
            "power": 26,  
            "hide_keyboard": "hide_keyboard"
        }

        if system_action in system_action_map:
            if system_action == "hide_keyboard":
                try:
                    self.device.driver.hide_keyboard()
                    self.logger.log_action("SYSTEM Hide Keyboard")
                    self.step_manager.add_step("Hid the keyboard")
                    return True
                except Exception as e:
                    print(f"[ActionHandler] Failed to hide keyboard: {e}")
                    return False
            else:
                try:
                    self.device.driver.press_keycode(system_action_map[system_action])
                    self.logger.log_action(f"SYSTEM {system_action.replace('_', ' ').title()}")
                    self.step_manager.add_step(f"Performed system action: {system_action}")
                    return True
                except Exception as e:
                    print(f"[ActionHandler] Failed to execute system action '{system_action}': {e}")
                    return False

        print(f"[ActionHandler] Unknown system action: {system_action}")
        return False

        

