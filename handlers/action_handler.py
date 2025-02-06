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
            "scroll": self.handle_scroll
        }

    def handle_action(self, action_data, screenshot_path):
        action = action_data.get("action", "").lower()
        handler = self.action_registry.get(action)

        if handler:
            result = handler(action_data, screenshot_path)
            self.action_data_logger.log_action(json.dumps(action_data))
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
            self.step_manager.add_step(f"Clicked on {desc}")
            return True
        print("[ActionHandler] ShowUI failed to find coordinates.")
        return False

    def handle_type(self, action_data, screenshot_path):
        text_to_type = action_data.get("desc", "")
        try:
            self.device.type_text(text_to_type)
            self.logger.log_action(f"TYPE {text_to_type}")
            self.step_manager.add_step(f"Typed '{text_to_type}'")
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

                scroll_distance = height // 3  
                end_x, end_y = start_x, start_y

                if direction == "up":
                    end_y = min(height, start_y + scroll_distance)
                elif direction == "down":
                    end_y = max(0, start_y - scroll_distance)
                elif direction == "left":
                    end_x = min(width, start_x + scroll_distance)
                elif direction == "right":
                    end_x = max(0, start_x - scroll_distance)
                else:
                    print(f"[DeviceController] Unknown scroll direction: {direction}")
                    return
                self.device.scroll(start_x, start_y, end_x, end_y)
                self.logger.log_action(f"SCROLL {direction} from {start_from}")
                self.step_manager.add_step(f"Scrolled {direction} from '{start_from}'")
                return True
            print(f"[ActionHandler] ShowUI failed to find coordinates for '{start_from}'.")
        else:
            print(f"[ActionHandler] Missing 'start_from' for scroll action.")
        return False
    

