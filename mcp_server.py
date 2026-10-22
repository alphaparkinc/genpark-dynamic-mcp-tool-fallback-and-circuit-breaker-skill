"""MCP server for Dynamic MCP Tool Fallback & Circuit Breaker."""
import sys
import json
from client import MCPToolCircuitBreaker

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "evaluate_mcp_circuit_breaker",
                "description": "Evaluates tool error history to trip circuit breakers and route to backup fallback tools",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "primary_tool": {"type": "string"},
                        "fallback_tool": {"type": "string"},
                        "call_history": {"type": "array"},
                        "failure_threshold": {"type": "number"}
                    },
                    "required": ["primary_tool", "fallback_tool", "call_history"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "evaluate_mcp_circuit_breaker":
            args = params.get("arguments", {})
            res = MCPToolCircuitBreaker.evaluate_tool_health(
                args.get("primary_tool", "primary"),
                args.get("fallback_tool", "fallback"),
                args.get("call_history", []),
                float(args.get("failure_threshold", 0.4))
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
