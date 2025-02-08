from openai import OpenAI
import base64

def encode_image(image_path: str) -> str:
    """
    Reads the image from the given path and returns its base64-encoded string.
    """
    with open(image_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')

class OpenAIClient:
    """
    Replaces the old QwenClient. This client uses the OpenAI Python SDK
    to communicate with a GPT-based model (potentially GPT-4 Vision).
    """

    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        """
        :param api_key: Your OpenAI API key.
        :param model_name: The model to use. E.g., 'gpt-3.5-turbo', 'gpt-4', or a hypothetical 'gpt-4-vision'.
        """
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def get_next_step(
        self,
        screenshot_path: str,
        system_prompt: str,
        user_prompt: str,
        previous_steps: str,
        user_feedback: str,
    ) -> str:
        """
        Calls the chosen OpenAI model to get the next suggested step in JSON form.

        :param screenshot_path: Local path to the screenshot for the vision model (if available).
        :param system_prompt: System-level instructions to constrain the model's output.
        :param user_prompt: The user's high-level test goal.
        :param previous_steps: A string containing all previous steps, for context.
        :return: Raw text from the model, which we expect to be JSON.
        """

        # Base64 encode the screenshot, in case you're using a vision model
        base64_image = encode_image(screenshot_path)
        last_3_steps = "\n".join(previous_steps.split("\n")[-3:])
        # Build the user message (with text + image data). 
        # If you do NOT have GPT-4 Vision, pass a text description instead of base64 data.
        user_content = [
            {
                "type": "text",
                "text": (
                    f"{user_prompt}\n"
                    f"Previous completed steps on the current device:\n{previous_steps}\n"
                    f"Last 3 Actions:\n{last_3_steps}\n"
                    f"User Feedback on previous steps:\n{user_feedback}"
                    "Analyze this image and provide the next important step as minimal JSON."
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        completion = self.client.chat.completions.create(
            model=self.model_name,    
            messages=messages,
            max_tokens=300,
            temperature=0.1
        )

        return completion.choices[0].message.content
