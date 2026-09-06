"""
Runtime Function Call Parameter Type Sanitizer and Coercion Engine.
Zero external dependencies, standard library only.
"""

from typing import Dict, List, Any, Optional

class ParameterTypeSanitizerClient:
    """
    Sanitizes LLM tool call inputs:
    - Coerces stringified numbers ("42" -> 42, "3.14" -> 3.14)
    - Coerces stringified booleans ("true", "1", "yes" -> True)
    - Clamps boundary ranges (min, max)
    - Injects default values for missing optional parameters
    """

    def __init__(self):
        pass

    def coerce_boolean(self, val: Any) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            return val.strip().lower() in ("true", "1", "yes", "t", "y")
        return False

    def sanitize_arguments(self, raw_args: Dict[str, Any], schema_properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes dictionary of raw_args according to schema rules.
        """
        cleaned = {}
        for p_name, prop_def in schema_properties.items():
            expected_type = prop_def.get("type")
            default_val = prop_def.get("default")
            
            if p_name not in raw_args:
                if default_val is not None:
                    cleaned[p_name] = default_val
                continue

            raw_val = raw_args[p_name]

            if expected_type == "integer":
                try:
                    cleaned[p_name] = int(raw_val)
                except (ValueError, TypeError):
                    cleaned[p_name] = default_val or 0
            elif expected_type == "number":
                try:
                    cleaned[p_name] = float(raw_val)
                except (ValueError, TypeError):
                    cleaned[p_name] = default_val or 0.0
            elif expected_type == "boolean":
                cleaned[p_name] = self.coerce_boolean(raw_val)
            elif expected_type == "string":
                cleaned[p_name] = str(raw_val) if raw_val is not None else (default_val or "")
            else:
                cleaned[p_name] = raw_val

            # Boundary clamping
            if "minimum" in prop_def and isinstance(cleaned.get(p_name), (int, float)):
                cleaned[p_name] = max(prop_def["minimum"], cleaned[p_name])
            if "maximum" in prop_def and isinstance(cleaned.get(p_name), (int, float)):
                cleaned[p_name] = min(prop_def["maximum"], cleaned[p_name])

        return cleaned
