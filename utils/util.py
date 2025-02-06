import jsonschema
import json

schema = {
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "desc": {"type": "string"},
        "start_from": {"type": "string"}
    },
    "required": ["action", "desc"]
}

def validate_openai_json(next_step_str):
    try:
        step_data = json.loads(next_step_str)
        jsonschema.validate(instance=step_data, schema=schema)
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
        print(f"[Validation Error] {e}")
