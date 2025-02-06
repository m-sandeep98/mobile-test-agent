import os
import json
from ast import literal_eval
from gradio_client import Client, handle_file
from PIL import Image

class ShowUiClient:
    def __init__(self):
        self.client = Client("showlab/ShowUI", hf_token=os.getenv("HUGGINGFACE_API_KEY"))

    def get_coordinate(self, screenshot_path: str, query: str, iterations: int = 1) -> tuple:
        """
        Calls ShowUI, which now returns a string like "[0.49, 0.06]".
        Parse that as fractional x,y in [0..1] and convert to pixels.
        """
        result = self.client.predict(
            image=handle_file(screenshot_path),
            query=query,
            iterations=1,
            is_example_image="False",
            api_name="/on_submit"
        )
        if not result or len(result) < 2:
            return (None, None)

        coord_str = result[1] 
        try:
            coords = literal_eval(coord_str)
            if not isinstance(coords, (list, tuple)) or len(coords) < 2:
                return (None, None)

            x_fraction = float(coords[0])  
            y_fraction = float(coords[1])

            # Convert fractional coords to pixel coords
            with Image.open(screenshot_path) as img:
                width, height = img.size

            pixel_x = int(x_fraction * width)
            pixel_y = int(y_fraction * height)

            return (pixel_x, pixel_y)
        except Exception as e:
            print(f"[ShowUiClient] Error parsing coordinates: {e}")
            return (None, None)
