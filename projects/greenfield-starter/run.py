#!/usr/bin/env python3
"""
Greenfield Project Starter - Main Entry Point

This script:
1. Loads project configuration from YAML files
2. Creates the team from team.yaml
3. Executes workflows from workflows/
4. Generates reports and saves outputs
"""

import sys
import os
import yaml
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import TeamAlpha modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole, Tool


def load_yaml(filepath: str):
    """Load YAML configuration file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def create_team_from_config(config_path: str) -> Team:
    """Create a Team instance from team.yaml configuration."""
    team_config = load_yaml(config_path)
    
    team_name = team_config.get('team_name', 'Development Team')
    team = Team(team_name)
    
    # Create agents from config
    for agent_config in team_config.get('agents', []):
        name = agent_config['name']
        role_str = agent_config['role']
        
        # Map role string to AgentRole enum
        role_map = {
            'engineer': AgentRole.ENGINEER,
            'code_reviewer': AgentRole.REVIEWER,
            'architect': AgentRole.ARCHITECT,
            'qa_engineer': AgentRole.TESTER,
            'product_manager': AgentRole.PM,
        }
        role = role_map.get(role_str, AgentRole.ENGINEER)
        
        agent = Agent(name=name, role=role)
        team.add_agent(agent)
        print(f"✓ Added agent: {name} ({role.value})")
    
    return team


def run_example_workflow(team: Team, project_config: dict):
    """Run an example workflow to demonstrate the team."""
    print("\n📋 Running example workflow...")
    print("=" * 60)
    
    # Get the architect
    architect = team.get_agent_by_role(AgentRole.ARCHITECT)
    if not architect:
        print("⚠️  No architect found in team")
        return
    
    # Create a simple task
    task = team.create_task(
        "design-1",
        f"Design the architecture for {project_config.get('name', 'the project')}"
    )
    team.assign_task(task.id, architect.name)
    
    # Execute
    print(f"\nAssigned task '{task.id}' to {architect.name}")
    print(f"Task: {task.description}\n")
    
    # Mock execution (since LLM might not be available)
    task.status = "completed"
    task.result = f"""
## Architecture Design

### Overview
This project follows a modular, scalable architecture.

### Key Components
1. **API Layer**: RESTful interface for clients
2. **Business Logic**: Core application logic
3. **Data Layer**: Database and persistence
4. **Services**: External integrations

### Design Decisions
- Use microservices for scalability
- Implement API versioning for compatibility
- Cache frequently accessed data
- Use async/await for I/O operations

### Next Steps
- [ ] Define API contracts (OpenAPI spec)
- [ ] Design database schema
- [ ] Implement core services
- [ ] Set up testing infrastructure
"""
    
    print(f"✓ Task completed by {architect.name}")
    print(f"\nResult:\n{task.result}")
    
    return task


def main():
    parser = argparse.ArgumentParser(
        description="TeamAlpha Greenfield Project Starter"
    )
    parser.add_argument(
        '--workflow',
        default='example',
        help="Workflow to execute (default: example)"
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Verbose output"
    )
    parser.add_argument(
        '--report',
        help="Save report to file"
    )
    
    args = parser.parse_args()
    
    # Paths
    base_dir = Path(__file__).parent
    project_config_path = base_dir / 'project.yaml'
    team_config_path = base_dir / 'team.yaml'
    
    print("🚀 TeamAlpha Greenfield Project Starter")
    print("=" * 60)
    
    # Load project config
    if not project_config_path.exists():
        print(f"❌ Project config not found: {project_config_path}")
        sys.exit(1)
    
    project_config = load_yaml(str(project_config_path))
    print(f"📦 Project: {project_config.get('name')}")
    print(f"   Version: {project_config.get('version')}")
    print(f"   Description: {project_config.get('description')}")
    print()
    
    # Create team
    if not team_config_path.exists():
        print(f"❌ Team config not found: {team_config_path}")
        sys.exit(1)
    
    team = create_team_from_team_config(str(team_config_path))
    print(f"\n✓ Team created: {len(team.agents)} agents\n")
    
    # Execute workflow
    if args.workflow == 'example':
        task = run_example_workflow(team, project_config)
    else:
        print(f"⚠️  Workflow '{args.workflow}' not found. Running example...")
        task = run_example_workflow(team, project_config)
    
    # Generate report
    if args.report:
        output_path = base_dir / args.report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report_content = f"""# {project_config.get('name')} - Project Report

**Generated**: {datetime.now().isoformat()}

## Project
- Name: {project_config.get('name')}
- Version: {project_config.get('version')}
- Description: {project_config.get('description')}

## Team
- Team Name: {team.name}
- Agents: {len(team.agents)}

### Team Members
"""
        for agent in team.agents.values():
            report_content += f"- {agent.name} ({agent.role.value})\n"
        
        report_content += f"""

## Execution Results

### Task: {task.id}
**Status**: {task.status}
**Assigned to**: {task.assigned_to}

**Result**:
{task.result}

## Summary
Project initialized and example workflow executed successfully.
"""
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        print(f"\n📄 Report saved to: {output_path}")
    
    print("\n✓ Workflow complete!")


if __name__ == "__main__":
    main()
