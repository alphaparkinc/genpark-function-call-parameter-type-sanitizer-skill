"""
MCP Server for genpark-function-call-parameter-type-sanitizer-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import ParameterTypeSanitizerClient

client = ParameterTypeSanitizerClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "sanitize_arguments",
                        "description": "Sanitize and coerce arguments against schema.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "raw_args": {"type": "object"},
                                "schema_properties": {"type": "object"}
                            },
                            "required": ["raw_args", "schema_properties"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "sanitize_arguments":
            res = client.sanitize_arguments(args.get("raw_args", {}), args.get("schema_properties", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
