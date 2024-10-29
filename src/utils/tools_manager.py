"""
Tools manager for handling OpenAI function calling tools.
This file contains the tools registry and execution logic.
"""

from typing import Dict, List, Callable
from dataclasses import dataclass
import json
from utils.logger import Logger

logger = Logger().get_logger(__name__)

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    implementation: Callable

class ToolsManager:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool):
        """Register a new tool with the manager."""
        logger.info(f"Registering tool: {tool.name}")
        self.tools[tool.name] = tool
    
    def get_tool_definitions(self) -> List[dict]:
        """Get OpenAI-compatible tool definitions for all registered tools."""
        return [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        } for tool in self.tools.values()]
    
    def execute_tool(self, name: str, arguments: str) -> str:
        """Execute a tool by name with the provided arguments."""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        
        logger.info(f"Executing tool: {name}")
        parsed_args = json.loads(arguments)
        return self.tools[name].implementation(parsed_args)

