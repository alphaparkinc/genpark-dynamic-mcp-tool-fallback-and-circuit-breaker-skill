"""Dynamic MCP Tool Fallback & Circuit Breaker.
100% Python Standard Library.
"""

class MCPToolCircuitBreaker:
    """Monitors MCP tool error rates and latencies, tripping circuit breakers and selecting healthy fallback tools."""

    @staticmethod
    def evaluate_tool_health(primary_tool: str, fallback_tool: str, call_history: list, failure_threshold: float = 0.4) -> dict:
        total = len(call_history)
        if total == 0:
            return {
                "active_tool": primary_tool,
                "circuit_state": "CLOSED",
                "failure_rate": 0.0,
                "failover_triggered": False
            }

        fails = sum(1 for c in call_history if c.get("status") in ("error", "timeout", "circuit_break"))
        rate = fails / float(total)

        if rate >= failure_threshold:
            state = "OPEN"
            active = fallback_tool
            failover = True
        else:
            state = "CLOSED"
            active = primary_tool
            failover = False

        return {
            "primary_tool": primary_tool,
            "active_tool": active,
            "circuit_state": state,
            "failure_rate": round(rate, 2),
            "failover_triggered": failover
        }
