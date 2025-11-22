#!/usr/bin/env python3
"""
Example workflow: API Design

This workflow demonstrates how to:
1. Create a team
2. Define tasks
3. Execute tasks with agents
4. Collect and report results
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole, Tool


def design_api():
    """Run an API design workflow."""
    
    # Create team
    team = Team("API Design Team")
    
    # Add agents
    architect = Agent("Eve", AgentRole.ARCHITECT)
    engineer = Agent("Alice", AgentRole.ENGINEER)
    reviewer = Agent("Bob", AgentRole.REVIEWER)
    
    team.add_agent(architect)
    team.add_agent(engineer)
    team.add_agent(reviewer)
    
    print(f"✓ Created team: {team.name}")
    print(f"  Agents: {', '.join([a.name for a in team.agents.values()])}\n")
    
    # Define workflow tasks
    tasks = [
        ("design-1", "Design REST API structure for a user management service"),
        ("design-2", "Define API endpoints (GET, POST, PUT, DELETE)"),
        ("review-1", "Review API design for security and best practices"),
    ]
    
    results = []
    
    for task_id, description in tasks:
        task = team.create_task(task_id, description)
        
        # Assign based on task type
        if "design" in task_id:
            assigned_to = "Eve"  # Architect
        else:
            assigned_to = "Bob"  # Reviewer
        
        team.assign_task(task_id, assigned_to)
        
        print(f"Task: {task_id}")
        print(f"  Description: {description}")
        print(f"  Assigned to: {assigned_to}\n")
        
        results.append(task)
    
    # Generate summary
    print("=" * 60)
    print("Workflow Summary")
    print("=" * 60)
    print(f"Team: {team.name}")
    print(f"Tasks: {len(results)}")
    print(f"Status: Complete")
    
    return team, results


if __name__ == "__main__":
    team, results = design_api()
