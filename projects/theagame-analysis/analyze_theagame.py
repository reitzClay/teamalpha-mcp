#!/usr/bin/env python3
"""Agent for analyzing the TheAgame repository using the HTTP LLM endpoint."""

import os
import json
from pathlib import Path
import sys
sys.path.insert(0, '/home/clay/Development/teamAlpha')

from src.teamalpha.client import TeamAlphaClient


def analyze_directory_structure(base_path: str, max_depth: int = 3, current_depth: int = 0) -> dict:
    """Recursively analyze directory structure."""
    if current_depth >= max_depth:
        return {}
    
    structure = {}
    try:
        for item in sorted(Path(base_path).iterdir()):
            if item.name.startswith('.'):
                continue
            if item.is_dir():
                subdir_count = len([d for d in item.iterdir() if d.is_dir()])
                file_count = len([f for f in item.iterdir() if f.is_file()])
                structure[item.name] = {
                    "type": "directory",
                    "files": file_count,
                    "subdirs": subdir_count,
                }
            else:
                structure[item.name] = {
                    "type": "file",
                    "size": item.stat().st_size,
                }
    except Exception as e:
        structure["error"] = str(e)
    return structure


def read_file_content(path: str, max_lines: int = 50) -> str:
    """Read file content with line limit."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[:max_lines]
            return ''.join(lines)
    except Exception as e:
        return f"Error reading file: {e}"


def main():
    """Main agent for TheAgame repo analysis."""
    
    repo_path = "/home/clay/Development/TheAgame"
    
    if not os.path.exists(repo_path):
        print(f"❌ Repository not found at {repo_path}")
        return
    
    print("=" * 80)
    print("🎮 TheAgame Repository Analysis Agent")
    print("=" * 80)
    print()
    
    # Initialize HTTP client
    try:
        client = TeamAlphaClient(base_url="http://localhost:8080")
        health = client.health()
        print(f"✅ Connected to LLM server: {health}")
    except Exception as e:
        print(f"⚠️  LLM server not available: {e}")
        print("Continuing with filesystem analysis only...\n")
        client = None
    
    # Step 1: Analyze directory structure
    print("📁 [STEP 1] Analyzing directory structure...")
    print()
    
    structure = analyze_directory_structure(repo_path)
    structure_str = json.dumps(structure, indent=2)
    print("Top-level Directory Structure:")
    for key, val in structure.items():
        if isinstance(val, dict):
            if val.get("type") == "directory":
                print(f"  📂 {key}/ (files: {val['files']}, subdirs: {val['subdirs']})")
            else:
                size_kb = val['size'] / 1024
                print(f"  📄 {key} ({size_kb:.1f} KB)")
    print()
    
    # Step 2: Read key files
    print("=" * 80)
    print("📄 [STEP 2] Reading key files...")
    print()
    
    key_files = [
        "README.md",
        "docker-compose.yml",
        "aBackend/package.json",
        "gameUI/package.json",
        "livekit-token-service/package.json",
    ]
    
    file_contents = {}
    for file_path in key_files:
        full_path = os.path.join(repo_path, file_path)
        if os.path.exists(full_path):
            print(f"📖 Reading: {file_path}")
            content = read_file_content(full_path, max_lines=20)
            file_contents[file_path] = content[:500]  # Limit to 500 chars for analysis
            print(f"   ✓ {len(content)} bytes")
        else:
            print(f"⏭️  {file_path} (not found)")
    
    print()
    
    # Step 3: AI Analysis
    if client:
        print("=" * 80)
        print("🧠 [STEP 3] Sending to AI for analysis...")
        print()
        
        analysis_prompt = f"""You are a software architecture expert. Analyze this repository:

STRUCTURE:
{structure_str}

README (first 500 chars):
{file_contents.get('README.md', 'Not found')[:500]}

KEY CONFIG FILES:
{json.dumps(file_contents, indent=2)[:1500]}

Provide a brief analysis covering:
1. Project type and purpose
2. Main components (aBackend, gameUI, livekit-token-service, etc.)
3. Technology stack
4. Architecture overview
5. Key recommendations

Keep it concise (5-10 sentences)."""

        try:
            print("📤 Sending request to LLM...\n")
            analysis = client.generate(prompt=analysis_prompt, max_tokens=512)
            print("📊 ANALYSIS RESULT:")
            print("-" * 80)
            print(analysis)
            print("-" * 80)
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    # Step 4: List all directories for deeper exploration
    print("\n" + "=" * 80)
    print("📂 [STEP 4] Full directory tree...")
    print()
    
    def print_tree(path, prefix="", max_depth=2, current_depth=0):
        if current_depth >= max_depth:
            return
        try:
            items = sorted(Path(path).iterdir())
            dirs = [i for i in items if i.is_dir() and not i.name.startswith('.')]
            for i, d in enumerate(dirs):
                is_last = i == len(dirs) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}{d.name}/")
                next_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(d, next_prefix, max_depth, current_depth + 1)
        except:
            pass
    
    print_tree(repo_path, max_depth=3)
    
    print("\n✅ Analysis complete!")
    print(f"\nTo dive deeper, the agent can inspect files in:")
    for key in structure.keys():
        if isinstance(structure[key], dict) and structure[key].get("type") == "directory":
            print(f"  - /home/clay/Development/TheAgame/{key}/")


if __name__ == "__main__":
    main()
