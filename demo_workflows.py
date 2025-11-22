#!/usr/bin/env python3
"""
TeamAlpha Interactive Client - Demonstration Script

Shows how to use the client programmatically for workflows.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.teamalpha.client import TeamAlphaClient
from src.teamalpha.agent import AgentRole


def demo_workflow():
    """Demonstrate a complete team workflow."""
    
    client = TeamAlphaClient("http://localhost:18080")
    
    print("🎯 TeamAlpha Workflow Demonstration\n")
    print("=" * 60)
    
    # Step 1: Check health
    print("\n1️⃣  Checking agent health...")
    health = client.health()
    print(f"   ✅ Agent Status: {health}\n")
    
    # Step 2: Get requirements from PM
    print("2️⃣  PM defines requirements...")
    pm_prompt = """You are a Product Manager. 
    Define requirements for building a user management system API.
    Include key features, user stories, and acceptance criteria."""
    print(f"   📝 Task: {pm_prompt[:60]}...")
    pm_response = client.generate(pm_prompt, max_tokens=300)
    print(f"   📋 Requirements:\n{pm_response[:200]}...\n")
    
    # Step 3: Architect designs system
    print("3️⃣  Architect designs the system...")
    arch_prompt = f"""You are a System Architect.
    Based on these requirements: {pm_response[:100]}...
    Design the database schema and API endpoints."""
    print(f"   🏗️  Task: Design architecture")
    arch_response = client.generate(arch_prompt, max_tokens=300)
    print(f"   🏛️  Design:\n{arch_response[:200]}...\n")
    
    # Step 4: Engineer implements
    print("4️⃣  Engineer implements...")
    eng_prompt = f"""You are a Backend Engineer.
    Based on this design: {arch_response[:100]}...
    Provide Python/FastAPI implementation code."""
    print(f"   💻 Task: Implement API")
    eng_response = client.generate(eng_prompt, max_tokens=300)
    print(f"   ✏️  Implementation:\n{eng_response[:200]}...\n")
    
    # Step 5: Reviewer reviews code
    print("5️⃣  Code Reviewer reviews...")
    reviewer_prompt = f"""You are a Code Reviewer.
    Review this implementation for quality: {eng_response[:100]}...
    Provide feedback on code quality, performance, and security."""
    print(f"   👀 Task: Review code")
    review_response = client.generate(reviewer_prompt, max_tokens=300)
    print(f"   📝 Review:\n{review_response[:200]}...\n")
    
    # Step 6: QA creates tests
    print("6️⃣  QA Engineer creates tests...")
    qa_prompt = f"""You are a QA Engineer.
    Based on this implementation: {eng_response[:100]}...
    Create test cases and edge cases to validate."""
    print(f"   🧪 Task: Create test cases")
    qa_response = client.generate(qa_prompt, max_tokens=300)
    print(f"   ✓ Tests:\n{qa_response[:200]}...\n")
    
    print("=" * 60)
    print("\n✅ Workflow Complete!")
    print("\n📊 Summary:")
    print(f"   • PM Requirements: {len(pm_response)} chars")
    print(f"   • Architecture Design: {len(arch_response)} chars")
    print(f"   • Implementation: {len(eng_response)} chars")
    print(f"   • Code Review: {len(review_response)} chars")
    print(f"   • QA Tests: {len(qa_response)} chars")
    print(f"   • Total Output: {len(pm_response + arch_response + eng_response + review_response + qa_response)} chars")


def demo_parallel_tasks():
    """Demonstrate parallel task execution."""
    
    client = TeamAlphaClient("http://localhost:18080")
    
    print("\n🔄 Parallel Task Execution\n")
    print("=" * 60)
    
    tasks = [
        ("Alice", "Engineer", "Design a login endpoint with password hashing"),
        ("Bob", "Reviewer", "Check for security vulnerabilities in authentication"),
        ("Eve", "Architect", "Design OAuth2 integration pattern"),
        ("Charlie", "QA", "List test cases for authentication flows"),
        ("Diana", "PM", "Define user authentication requirements"),
    ]
    
    print("\n📤 Sending parallel tasks to all agents...\n")
    
    results = {}
    for name, role, task in tasks:
        print(f"   → {name} ({role}): {task[:40]}...")
        full_prompt = f"You are a {role}. {task}"
        response = client.generate(full_prompt, max_tokens=150)
        results[name] = response
        print(f"     ✅ Completed\n")
    
    print("=" * 60)
    print("\n📊 Results:")
    for name, response in results.items():
        print(f"\n{name}:")
        print(f"  {response[:150]}...")
    
    print(f"\n✅ All {len(results)} tasks completed!")


def main():
    """Run demonstrations."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="TeamAlpha Workflow Demonstrations")
    parser.add_argument("--workflow", action="store_true", help="Run full workflow demo")
    parser.add_argument("--parallel", action="store_true", help="Run parallel tasks demo")
    parser.add_argument("--all", action="store_true", help="Run all demos")
    
    args = parser.parse_args()
    
    if not (args.workflow or args.parallel or args.all):
        print("Usage: python3 demo_workflows.py [--workflow] [--parallel] [--all]")
        print("\nExamples:")
        print("  python3 demo_workflows.py --workflow    # Show full team workflow")
        print("  python3 demo_workflows.py --parallel    # Show parallel execution")
        print("  python3 demo_workflows.py --all         # Run all demos")
        sys.exit(1)
    
    try:
        if args.workflow or args.all:
            demo_workflow()
        if args.parallel or args.all:
            demo_parallel_tasks()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
