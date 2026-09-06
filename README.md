# GenPark AI Agent Skill - Function Call Parameter Sanitizer

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Runtime function argument coercion, boundary clamping, and type sanitization preventing TypeError crashes during LLM tool dispatch.

```mermaid
flowchart LR
    A[Raw LLM String Arguments] --> B[Type Coercion Engine]
    B --> C[Boundary Clamping Min/Max]
    C --> D[Default Fallback Injection]
    D --> E[Type-Safe Tool Execution]
```

## Features
- **String-to-Numeric & Bool Coercion**: Handles `"true"`, `"yes"`, `"42"`, `"3.14"`.
- **Range Clamping**: Ensures numeric inputs stay strictly within legal bounds.
- **Zero External Dependencies**: Python 3.9+ standard library.

## Quickstart
```python
from client import ParameterTypeSanitizerClient

sanitizer = ParameterTypeSanitizerClient()
clean_args = sanitizer.sanitize_arguments(raw_llm_args, schema)
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
