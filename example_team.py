#!/usr/bin/env python3
"""Example: A software team building a simple feature."""

import os
from src.teamalpha.agent import Agent, AgentRole, Tool, Message
from src.teamalpha.team import Team, Task


def git_command(cmd: str) -> str:
    """Simulate a git command."""
    return f"[Git executed]: {cmd}"


def write_file(filename: str, content: str) -> str:
    """Simulate writing a file."""
    return f"File {filename} written with {len(content)} chars"


def run_tests(pattern: str) -> str:
    """Simulate running tests."""
    return f"Ran tests matching {pattern}: 5 passed, 0 failed"


def code_review(branch: str) -> str:
    """Simulate code review."""
    return f"Code review of {branch}: Approved with minor suggestions"


def main():
    """Run the example software team."""

    # Create the team
    team = Team("TeamAlpha")

    # Add agents
    engineer = Agent(name="Alice", role=AgentRole.ENGINEER)
    engineer.add_tool(
        Tool(
            name="write_code",
            description="Write or edit code files",
            func=write_file,
            required_args=["filename", "content"],
        )
    )
    engineer.add_tool(
        Tool(
            name="run_git",
            description="Run git commands (commit, push, pull)",
            func=git_command,
            required_args=["cmd"],
        )
    )
    team.add_agent(engineer)

    reviewer = Agent(name="Bob", role=AgentRole.REVIEWER)
    reviewer.add_tool(
        Tool(
            name="review_code",
            description="Review a code branch",
            func=code_review,
            required_args=["branch"],
        )
    )
    team.add_agent(reviewer)

    tester = Agent(name="Charlie", role=AgentRole.TESTER)
    tester.add_tool(
        Tool(
            name="run_tests",
            description="Run test suite",
            func=run_tests,
            required_args=["pattern"],
        )
    )
    team.add_agent(tester)

    pm = Agent(name="Diana", role=AgentRole.PM)
    team.add_agent(pm)

    print(f"\n{team}\n")
    print("=" * 70)

    # Create a workflow
    print("\n[WORKFLOW] Building a feature: Add user authentication\n")

    # Task 1: Design
    task1 = team.create_task(
        "design-auth",
        "Design a user authentication system with login/logout endpoints. Consider security best practices.",
    )
    team.assign_task("design-auth", "Alice")
    result1 = team.execute_task("design-auth")
    print(f"\n[Task Result]\n{result1.result[:500]}...\n")

    # Task 2: Code review
    task2 = team.create_task(
        "review-auth",
        "Review the authentication code for security vulnerabilities.",
    )
    team.assign_task("review-auth", "Bob")
    result2 = team.execute_task("review-auth")
    print(f"\n[Task Result]\n{result2.result[:500]}...\n")

    # Task 3: Testing
    task3 = team.create_task(
        "test-auth",
        "Write and run comprehensive tests for the authentication module.",
    )
    team.assign_task("test-auth", "Charlie")
    result3 = team.execute_task("test-auth")
    print(f"\n[Task Result]\n{result3.result[:500]}...\n")

    # Final report
    print("\n" + "=" * 70)
    print("\n[TEAM STATUS REPORT]\n")
    status = team.get_status_report()
    print(f"Team: {status['team']}")
    print(f"Agents: {len(status['agents'])}")
    for agent_info in status["agents"]:
        print(f"  - {agent_info['name']} ({agent_info['role']})")
    print(f"\nTasks completed: {sum(1 for t in status['tasks'] if t['status'] == 'completed')}")
    print(f"Total messages: {status['messages']}")

    print("\n[MESSAGE LOG - Last 5 messages]\n")
    for msg in team.message_log[-5:]:
        print(f"{msg.sender} ({msg.role.value}): {msg.content[:100]}...")


if __name__ == "__main__":
    main()
