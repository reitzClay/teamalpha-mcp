#!/usr/bin/env python3
"""
Specialized agent for analyzing TheAgame PRODUCTION build.
Includes live service analysis, logs, metrics, and deployment state.
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import sys
sys.path.insert(0, '/home/clay/Development/teamAlpha')

from src.teamalpha.client import TeamAlphaClient


def get_git_info(repo_path: str) -> dict:
    """Get git status and recent commits."""
    try:
        os.chdir(repo_path)
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()[:8]
        status = subprocess.check_output(['git', 'status', '--porcelain']).decode().strip()
        log = subprocess.check_output(['git', 'log', '--oneline', '-5']).decode().strip()
        
        return {
            "branch": branch,
            "commit": commit,
            "status": status if status else "clean",
            "recent_commits": log.split('\n')
        }
    except Exception as e:
        return {"error": str(e)}


def analyze_logs(log_dir: str) -> dict:
    """Analyze logs in the production build."""
    logs_info = {}
    if not os.path.exists(log_dir):
        return {"error": f"Log directory not found: {log_dir}"}
    
    try:
        for log_file in sorted(Path(log_dir).glob('*.log'))[:10]:  # Last 10 log files
            size_kb = log_file.stat().st_size / 1024
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
            
            # Get last few lines
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[-5:]
                    last_lines = ''.join(lines)
            except:
                last_lines = ""
            
            logs_info[log_file.name] = {
                "size_kb": round(size_kb, 2),
                "modified": mtime,
                "last_lines": last_lines[:200]
            }
    except Exception as e:
        logs_info["error"] = str(e)
    
    return logs_info


def analyze_data_directory(data_dir: str) -> dict:
    """Analyze data directory (DB, cache, volumes, etc.)."""
    data_info = {}
    if not os.path.exists(data_dir):
        return {"error": f"Data directory not found: {data_dir}"}
    
    try:
        for item in sorted(Path(data_dir).iterdir()):
            if item.is_dir():
                file_count = len(list(item.glob('*')))
                total_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file()) / (1024*1024)
                data_info[item.name] = {
                    "type": "directory",
                    "files": file_count,
                    "size_mb": round(total_size, 2),
                    "subdirs": [d.name for d in item.iterdir() if d.is_dir()][:5]
                }
            else:
                size_mb = item.stat().st_size / (1024*1024)
                data_info[item.name] = {
                    "type": "file",
                    "size_mb": round(size_mb, 2)
                }
    except Exception as e:
        data_info["error"] = str(e)
    
    return data_info


def analyze_deployment_configs(repo_path: str) -> dict:
    """Analyze deployment-specific configs."""
    configs = {}
    
    # Check docker-compose files
    compose_files = [
        ("dev", os.path.join(repo_path, "docker-compose.yml")),
        ("prod", os.path.join(repo_path, "docker-compose.prod.yml"))
    ]
    
    for env_type, compose_path in compose_files:
        if os.path.exists(compose_path):
            try:
                with open(compose_path, 'r') as f:
                    content = f.read()
                    # Extract services
                    services = []
                    for line in content.split('\n'):
                        if line.strip().startswith('- ') or (line.strip() and not line.startswith(' ')):
                            if 'image:' in line or 'build:' in line or 'ports:' in line:
                                services.append(line.strip()[:80])
                    
                    configs[f"docker-compose.{env_type}"] = {
                        "path": compose_path,
                        "size": os.path.getsize(compose_path),
                        "services": services[:10]
                    }
            except Exception as e:
                configs[f"docker-compose.{env_type}"] = {"error": str(e)}
    
    # Check .env file
    env_file = os.path.join(repo_path, ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                env_vars = {}
                for line in f.readlines():
                    if line.strip() and not line.startswith('#'):
                        key = line.split('=')[0] if '=' in line else ""
                        if key:
                            env_vars[key] = "***"  # Hide values
                configs["env_vars"] = env_vars
        except Exception as e:
            configs["env_file_error"] = str(e)
    
    return configs


def main():
    """Analyze production TheAgame build."""
    
    prod_path = "/home/clay/Projects/TheAgame"
    
    if not os.path.exists(prod_path):
        print(f"❌ Production build not found at {prod_path}")
        return
    
    print("=" * 80)
    print("🚀 TheAgame PRODUCTION Build Analysis")
    print("=" * 80)
    print(f"📍 Location: {prod_path}")
    print(f"🕐 Analyzed at: {datetime.now().isoformat()}")
    print()
    
    # Initialize HTTP client
    try:
        client = TeamAlphaClient(base_url="http://localhost:8080")
        health = client.health()
        print(f"✅ Connected to LLM server")
        use_llm = True
    except Exception as e:
        print(f"⚠️  LLM server not available: {e}")
        use_llm = False
    
    print()
    print("=" * 80)
    print("📊 [STEP 1] Git Status & Version Control")
    print("=" * 80)
    print()
    
    git_info = get_git_info(prod_path)
    print(f"📌 Branch: {git_info.get('branch', 'unknown')}")
    print(f"📌 Commit: {git_info.get('commit', 'unknown')}")
    print(f"📌 Status: {git_info.get('status', 'unknown')}")
    print()
    print("Recent commits:")
    for commit in git_info.get('recent_commits', [])[:5]:
        print(f"  {commit}")
    print()
    
    print("=" * 80)
    print("📁 [STEP 2] Directory Structure & Data")
    print("=" * 80)
    print()
    
    # List main directories
    print("Main directories:")
    for item in sorted(Path(prod_path).iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            file_count = len(list(item.glob('*')))
            print(f"  📂 {item.name}/ ({file_count} items)")
    print()
    
    # Analyze data directory
    data_dir = os.path.join(prod_path, "data")
    print("Data directory structure:")
    data_info = analyze_data_directory(data_dir)
    for key, val in data_info.items():
        if isinstance(val, dict) and "error" not in val:
            if val.get("type") == "directory":
                print(f"  📂 {key}/ ({val['files']} files, {val['size_mb']} MB)")
            else:
                print(f"  📄 {key} ({val['size_mb']} MB)")
    print()
    
    print("=" * 80)
    print("📝 [STEP 3] Logs & Runtime State")
    print("=" * 80)
    print()
    
    log_dir = os.path.join(prod_path, "log")
    logs_info = analyze_logs(log_dir)
    print(f"Log files in {log_dir}:")
    for log_name, log_data in list(logs_info.items())[:5]:
        if isinstance(log_data, dict) and "error" not in log_data:
            print(f"  📄 {log_name} ({log_data['size_kb']} KB, {log_data['modified'][:10]})")
    print()
    
    print("=" * 80)
    print("⚙️  [STEP 4] Deployment Configuration")
    print("=" * 80)
    print()
    
    deploy_info = analyze_deployment_configs(prod_path)
    for config_name, config_data in deploy_info.items():
        if isinstance(config_data, dict) and "error" not in config_data:
            print(f"  {config_name}:")
            if config_name.startswith("docker-compose"):
                print(f"    - Size: {config_data.get('size', 0)} bytes")
                if config_data.get('services'):
                    print(f"    - Services/Config lines: {len(config_data['services'])}")
            elif config_name == "env_vars":
                print(f"    - Variables: {len(config_data)}")
    print()
    
    # LLM Analysis
    if use_llm:
        print("=" * 80)
        print("🧠 [STEP 5] AI Analysis of Production State")
        print("=" * 80)
        print()
        
        analysis_prompt = f"""You are a DevOps/SRE expert analyzing a production deployment.

GIT STATUS:
{json.dumps(git_info, indent=2)[:500]}

DATA DIRECTORIES:
{json.dumps(data_info, indent=2)[:800]}

DEPLOYMENT CONFIG:
{json.dumps({k: v for k, v in deploy_info.items() if k.startswith('docker-compose')}, indent=2)[:600]}

Provide a brief production health assessment covering:
1. Deployment freshness (how recent is the commit?)
2. Data volume assessment (normal/abnormal sizes?)
3. Deployment strategy (docker-compose.yml vs docker-compose.prod.yml)
4. Health indicators (anything concerning in the config?)
5. Recommendations for monitoring/logging

Keep it concise (6-8 sentences)."""

        try:
            print("📤 Sending production state to LLM...\n")
            analysis = client.generate(prompt=analysis_prompt, max_tokens=512)
            print("📊 PRODUCTION ANALYSIS:")
            print("-" * 80)
            print(analysis)
            print("-" * 80)
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    print()
    print("=" * 80)
    print("✅ Production Analysis Complete!")
    print("=" * 80)
    print()
    print("Key Files Agent Can Inspect:")
    print("  - /home/clay/Projects/TheAgame/aBackend/src/")
    print("  - /home/clay/Projects/TheAgame/gameUI/src/")
    print("  - /home/clay/Projects/TheAgame/docker-compose.prod.yml")
    print("  - /home/clay/Projects/TheAgame/.env")
    print("  - /home/clay/Projects/TheAgame/log/")
    print()


if __name__ == "__main__":
    main()
