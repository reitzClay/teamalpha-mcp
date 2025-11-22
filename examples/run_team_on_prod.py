#!/usr/bin/env python3
"""
Run TeamAlpha agents to analyze the production TheAgame repository.

This script creates a small team, registers a workflow-analysis tool (wrapping
the existing `workflow_analyzer.py`), stubs the agents' LLM invoke method to
call the tool (so this runs without a live Ollama server), assigns a task,
and executes it. Results are printed and written to disk.
"""

import sys
import types

# Provide a lightweight stub for `langchain_ollama` so the agents can be
# instantiated without installing the real dependency during this local run.
mod = types.ModuleType("langchain_ollama")
class OllamaLLM:
    def __init__(self, model="llama3", base_url="http://ollama:11434"):
        self.model = model
        self.base_url = base_url
    def invoke(self, prompt: str):
        # Default stub; will be monkeypatched per-agent later in this script.
        return "[STUB LLM] No action taken."
mod.OllamaLLM = OllamaLLM
sys.modules["langchain_ollama"] = mod

from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole, Tool, Message
import workflow_analyzer as wa
import time
import os


def workflow_tool(path: str) -> str:
    """Wrapper around workflow_analyzer to run a full analysis.

    Returns a short summary and the path to the saved full report.
    """
    # Ensure absolute path
    repo_path = os.path.abspath(path)
    # Use analyzer to produce dev and prod states (dev path comes from module)
    dev_state = wa.analyze_workflow(wa.DEV_PATH)
    prod_state = wa.analyze_workflow(repo_path)
    report = wa.generate_workflow_report(dev_state, prod_state)
    recommendations = wa.generate_recommendations(dev_state, prod_state)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_path = f"/home/clay/Development/teamAlpha/TEAM_RUN_REPORT_{timestamp}.md"
    with open(out_path, "w") as f:
        f.write(report)
        f.write("\n\n")
        f.write(recommendations)

    summary = (
        f"Workflow analysis complete for {repo_path}.\n"
        f"Saved full report to: {out_path}\n"
        f"Summary (first 400 chars):\n{report[:400]}"
    )
    return summary


def make_agent(name: str, role: AgentRole) -> Agent:
    a = Agent(name=name, role=role)
    return a


def main():
    target = "/home/clay/Projects/TheAgame"
    team = Team("TeamAlpha-Prod")

    # Create agents
    eng = make_agent("Alice", AgentRole.ENGINEER)
    rev = make_agent("Bob", AgentRole.REVIEWER)
    arch = make_agent("Eve", AgentRole.ARCHITECT)
    qa = make_agent("Charlie", AgentRole.TESTER)
    pm = make_agent("Diana", AgentRole.PM)

    for a in (eng, rev, arch, qa, pm):
        team.add_agent(a)

    # Register the workflow tool on the architect and engineer
    wf_tool = Tool(
        name="workflow_analyze",
        description="Run repository workflow analysis and produce recommendations",
        func=lambda path: workflow_tool(path),
        required_args=["path"],
    )

    arch.add_tool(wf_tool)
    eng.add_tool(wf_tool)

    # Monkeypatch agents' LLM invoke so that they request the workflow tool
    # directly. This avoids needing a running Ollama server for this run.
    tool_call = '[TOOL: workflow_analyze, ARGS: {"path": "/home/clay/Projects/TheAgame"}]'
    for a in (arch, eng):
        a.llm.invoke = lambda prompt, _tool_call=tool_call: _tool_call

    # Create and assign task
    task = team.create_task("prod-analysis-1", f"Analyze repository at {target}")
    team.assign_task(task.id, "Eve")

    # Execute the task
    print("Starting execution of workflow analysis task...")
    executed = team.execute_task(task.id)

    print("\nExecution complete. Task result summary:\n")
    # Print a trimmed result
    print(executed.result[:2000])

    status = team.get_status_report()
    print("\nTeam status:\n", status)


if __name__ == "__main__":
    main()
