"""
Demonstration of genpark-function-call-parameter-type-sanitizer-skill
"""

from client import ParameterTypeSanitizerClient

def main():
    sanitizer = ParameterTypeSanitizerClient()

    schema = {
        "user_id": {"type": "integer", "minimum": 1},
        "temperature": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.7},
        "debug_mode": {"type": "boolean", "default": False},
        "query": {"type": "string"}
    }

    # Malformed LLM inputs with stringified numbers and string boolean
    raw_llm_args = {
        "user_id": "-5",            # Below minimum 1
        "temperature": "1.5",       # Above maximum 1.0
        "debug_mode": "yes",        # String boolean
        "query": 12345              # Number instead of string
    }

    cleaned = sanitizer.sanitize_arguments(raw_llm_args, schema)
    print("=== SANITIZED FUNCTION CALL ARGUMENTS ===")
    print("User ID (clamped to min 1):", cleaned["user_id"])
    print("Temperature (clamped to max 1.0):", cleaned["temperature"])
    print("Debug Mode (coerced boolean):", cleaned["debug_mode"])
    print("Query (coerced string):", cleaned["query"])

if __name__ == "__main__":
    main()
