from fastmcp import FastMCP
from core.scanner_pii import PIIScanner
from core.attack_engine import AdaptiveAttacker
import asyncio

# Initialize the MCP Server
mcp = FastMCP("ART-T Red Teaming")
scanner = PIIScanner()
attacker = AdaptiveAttacker()

@mcp.tool()
async def scan_text_for_pii(text: str) -> str:
    """Scans input text for PII using Regex, NER, and Semantic Analysis."""
    report = await scanner.scan(text)
    return str(report)

@mcp.tool()
async def run_adaptive_attack(target_goal: str) -> str:
    """Runs a multi-step LangGraph attack to achieve a specific goal (e.g., 'extract password')."""
    result = await attacker.run_campaign(target_goal)
    return str(result)

if __name__ == "__main__":
    mcp.run()