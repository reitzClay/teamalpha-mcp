#!/usr/bin/env python3
"""Team orchestration and coordination logic."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from src.teamalpha.agent import Agent, AgentRole, Message, Tool
import json
import time


@dataclass
class Task:
    """A task assigned to an agent or team."""

    id: str
    description: str
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, blocked
    result: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return {
            "id": self.id,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class Team:
    """A team of collaborative agents."""

    def __init__(self, name: str):
        """Initialize a team."""
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.message_log: List[Message] = []
        self.context = ""

    def add_agent(self, agent: Agent):
        """Add an agent to the team."""
        self.agents[agent.name] = agent
        agent.context = f"Team: {self.name}"

    def get_agent_by_role(self, role: AgentRole) -> Optional[Agent]:
        """Get first agent with a given role."""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None

    def broadcast_message(self, message: Message):
        """Broadcast a message to all team members."""
        self.message_log.append(message)
        for agent in self.agents.values():
            agent.add_memory(message)

    def create_task(self, task_id: str, description: str) -> Task:
        """Create a new task."""
        task = Task(id=task_id, description=description)
        self.tasks[task_id] = task
        return task

    def assign_task(self, task_id: str, agent_name: str):
        """Assign a task to an agent."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")

        task = self.tasks[task_id]
        task.assigned_to = agent_name
        task.status = "assigned"

        # Notify team
        msg = Message(
            sender="SYSTEM",
            role=AgentRole.PM,
            content=f"Task {task_id} assigned to {agent_name}: {task.description}",
        )
        self.broadcast_message(msg)

    def execute_task(self, task_id: str) -> Task:
        """Execute a task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        if not task.assigned_to:
            raise ValueError(f"Task {task_id} not assigned")

        agent = self.agents[task.assigned_to]
        task.status = "in_progress"

        # Notify team
        msg = Message(
            sender="SYSTEM",
            role=AgentRole.PM,
            content=f"Executing task {task_id} with {agent.name}",
        )
        self.broadcast_message(msg)

        # Execute
        result = agent.execute(task.description)
        task.result = result
        task.status = "completed"
        task.completed_at = time.time()

        # Notify team
        msg = Message(
            sender=agent.name,
            role=agent.role,
            content=f"Completed task {task_id}. Result: {result[:500]}...",
        )
        self.broadcast_message(msg)

        return task

    def get_status_report(self) -> Dict[str, Any]:
        """Get a status report of the team."""
        return {
            "team": self.name,
            "agents": [
                {"name": a.name, "role": a.role.value}
                for a in self.agents.values()
            ],
            "tasks": [t.to_dict() for t in self.tasks.values()],
            "messages": len(self.message_log),
        }

    def __repr__(self) -> str:
        return f"Team({self.name}, agents={len(self.agents)}, tasks={len(self.tasks)})"
