"""Example usage for Dynamic MCP Tool Fallback & Circuit Breaker."""
from client import MCPToolCircuitBreaker

if __name__ == "__main__":
    history = [{"status": "error"}, {"status": "timeout"}, {"status": "ok"}, {"status": "error"}]
    res = MCPToolCircuitBreaker.evaluate_tool_health("primary_db_tool", "backup_db_tool", history)
    print("Active Tool:", res["active_tool"], "Circuit State:", res["circuit_state"])
