#!/usr/bin/env python3
"""Base agent class and role definitions for the software team."""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from langchain_ollama import OllamaLLM
import json


class AgentRole(Enum):
    """Enumeration of software team roles."""

    ENGINEER = "engineer"
    REVIEWER = "code_reviewer"
    ARCHITECT = "architect"
    TESTER = "qa_engineer"
    PM = "product_manager"


@dataclass
class Message:
    """A message in the team communication."""

    sender: str
    role: AgentRole
    content: str
    timestamp: float = field(default_factory=lambda: __import__("time").time())

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dict."""
        return {
            "sender": self.sender,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
        }


@dataclass
class Tool:
    """A tool available to agents."""

    name: str
    description: str
    func: Callable
    required_args: List[str] = field(default_factory=list)

    def invoke(self, **kwargs) -> str:
        """Invoke the tool."""
        try:
            result = self.func(**kwargs)
            return json.dumps({"success": True, "result": result})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})


class Agent:
    """Base agent class for software team members."""

    def __init__(
        self,
        name: str,
        role: AgentRole,
        llm_model: str = "llama3",
        ollama_host: str = "http://ollama:11434",
    ):
        """
        Initialize an agent.

        Args:
            name: Agent name (e.g., "Alice")
            role: Agent role (engineer, reviewer, etc.)
            llm_model: LLM model name
            ollama_host: Ollama server URL
        """
        self.name = name
        self.role = role
        self.llm = OllamaLLM(model=llm_model, base_url=ollama_host)
        self.tools: Dict[str, Tool] = {}
        self.memory: List[Message] = []
        self.context = ""

    def add_tool(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def add_memory(self, message: Message):
        """Add a message to memory."""
        self.memory.append(message)

    def get_memory_summary(self, last_n: int = 10) -> str:
        """Get a summary of recent messages."""
        recent = self.memory[-last_n:]
        summary = "\n".join(
            [
                f"[{m.sender} ({m.role.value})]: {m.content[:200]}"
                for m in recent
            ]
        )
        return summary or "No messages yet."

    def build_system_prompt(self) -> str:
        """Build the system prompt for this agent."""
        tools_desc = "\n".join(
            [f"- {t.name}: {t.description}" for t in self.tools.values()]
        )
        return f"""You are {self.name}, a {self.role.value} in a software team.

Your responsibilities:
- Produce clear, concise work aligned with your role
- Use tools when necessary
- Communicate decisions and blockers to the team

Available tools:
{tools_desc or "None yet"}

Recent team memory:
{self.get_memory_summary()}

{self.context}
"""

    def think(self, task: str) -> str:
        """
        Invoke the LLM to think about a task.

        Args:
            task: The task description

        Returns:
            LLM response
        """
        prompt = f"{self.build_system_prompt()}\n\nTask: {task}"
        return self.llm.invoke(prompt)

    def parse_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse tool calls from LLM response (simple regex-based parser).

        Expects format: [TOOL: tool_name, ARGS: {"key": "value"}]
        """
        import re

        tool_calls = []
        pattern = r"\[TOOL:\s*(\w+),\s*ARGS:\s*({[^}]+})\]"
        for match in re.finditer(pattern, response):
            tool_name = match.group(1)
            args_str = match.group(2)
            try:
                args = json.loads(args_str)
                tool_calls.append({"tool": tool_name, "args": args})
            except json.JSONDecodeError:
                pass

        return tool_calls

    def execute(self, task: str) -> str:
        """
        Execute a task: think, parse tool calls, and return result.

        Args:
            task: The task description

        Returns:
            Execution result
        """
        response = self.think(task)
        tool_calls = self.parse_tool_calls(response)

        if tool_calls:
            for call in tool_calls:
                tool_name = call["tool"]
                args = call["args"]
                if tool_name in self.tools:
                    result = self.tools[tool_name].invoke(**args)
                    response += f"\n[Tool Result ({tool_name})]: {result}"

        return response

    def __repr__(self) -> str:
        return f"Agent({self.name}, {self.role.value})"
