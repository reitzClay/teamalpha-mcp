#!/usr/bin/env python3
"""
Workflow Analysis Agent
Analyzes git workflow state and suggests improvements for dev→prod transitions
with Docker isolation constraints.
"""

import os
import subprocess
import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Development and production build paths
DEV_PATH = "/home/clay/Development/TheAgame"
PROD_PATH = "/home/clay/Projects/TheAgame"
TEAMALPHA_PATH = "/home/clay/Development/teamAlpha"


@dataclass
class BranchInfo:
    """Information about a git branch"""
    name: str
    is_local: bool
    is_remote: bool
    is_head: bool
    last_commit: Optional[str] = None
    commit_message: Optional[str] = None
    commit_date: Optional[str] = None


@dataclass
class WorkflowState:
    """Current workflow state analysis"""
    repo_path: str
    current_branch: str
    branches: dict
    uncommitted_changes: list
    untracked_files: list
    divergence_from_origin: int
    stale_branches: list
    merge_conflicts: list


def run_git_command(cmd: str, cwd: str) -> str:
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_branch_health(repo_path: str) -> tuple[list, list]:
    """Analyze which branches are stale and which are active"""
    # Get last commit date for each branch
    branches_output = run_git_command(
        "git for-each-ref --sort=-committerdate --format='%(refname:short)|%(committerdate:short)|%(subject)' refs/heads/",
        repo_path
    )
    
    active_branches = []
    stale_branches = []
    
    for line in branches_output.split("\n"):
        if not line.strip():
            continue
        try:
            branch, date, subject = line.split("|", 2)
            # Parse date to check if stale (> 30 days)
            import datetime
            branch_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.date.today()
            days_old = (today - branch_date).days
            
            if days_old > 30:
                stale_branches.append({
                    "name": branch,
                    "last_commit": date,
                    "days_old": days_old,
                    "subject": subject[:50]
                })
            else:
                active_branches.append({
                    "name": branch,
                    "last_commit": date,
                    "days_old": days_old,
                    "subject": subject[:50]
                })
        except:
            pass
    
    return active_branches, stale_branches


def get_uncommitted_changes(repo_path: str) -> list:
    """Get list of uncommitted changes"""
    status_output = run_git_command("git status --porcelain", repo_path)
    changes = []
    for line in status_output.split("\n"):
        if line.strip():
            status_code = line[:2]
            filepath = line[3:]
            changes.append({"status": status_code, "file": filepath})
    return changes


def get_branch_list(repo_path: str) -> dict:
    """Get all branches (local and remote)"""
    branches_output = run_git_command("git branch -a", repo_path)
    branches = {}
    
    for line in branches_output.split("\n"):
        if not line.strip():
            continue
        is_current = line.startswith("*")
        branch_name = line.replace("*", "").strip()
        
        # Get last commit info
        commit_output = run_git_command(
            f"git log -1 --format='%h|%ai|%s' {branch_name}",
            repo_path
        )
        
        if "|" in commit_output:
            commit_hash, commit_date, subject = commit_output.split("|", 2)
            branches[branch_name] = {
                "current": is_current,
                "commit": commit_hash,
                "date": commit_date,
                "subject": subject
            }
    
    return branches


def analyze_workflow(repo_path: str) -> WorkflowState:
    """Comprehensive workflow analysis"""
    current_branch = run_git_command("git rev-parse --abbrev-ref HEAD", repo_path)
    branches = get_branch_list(repo_path)
    uncommitted = get_uncommitted_changes(repo_path)
    active, stale = analyze_branch_health(repo_path)
    
    # Check for untracked files
    untracked_output = run_git_command(
        "git ls-files --others --exclude-standard",
        repo_path
    )
    untracked = [f for f in untracked_output.split("\n") if f.strip()]
    
    # Check divergence from origin
    divergence_output = run_git_command(
        f"git rev-list --left-right --count origin/{current_branch}...{current_branch}",
        repo_path
    )
    
    divergence = 0
    if divergence_output and "|" in divergence_output:
        try:
            behind, ahead = map(int, divergence_output.split())
            divergence = behind + ahead
        except:
            pass
    
    return WorkflowState(
        repo_path=repo_path,
        current_branch=current_branch,
        branches=branches,
        uncommitted_changes=uncommitted,
        untracked_files=untracked,
        divergence_from_origin=divergence,
        stale_branches=stale,
        merge_conflicts=[]
    )


def generate_workflow_report(dev_state: WorkflowState, prod_state: WorkflowState) -> str:
    """Generate comprehensive workflow analysis report"""
    
    report = []
    report.append("=" * 80)
    report.append("WORKFLOW ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")
    
    # SECTION 1: DEV BUILD STATUS
    report.append("📁 DEVELOPMENT BUILD STATUS")
    report.append("-" * 80)
    report.append(f"Location: {dev_state.repo_path}")
    report.append(f"Current Branch: {dev_state.current_branch}")
    report.append(f"Uncommitted Changes: {len(dev_state.uncommitted_changes)}")
    report.append(f"Untracked Files: {len(dev_state.untracked_files)}")
    report.append(f"Stale Branches (>30 days): {len(dev_state.stale_branches)}")
    report.append("")
    
    if dev_state.uncommitted_changes:
        report.append("  Uncommitted Changes:")
        for change in dev_state.uncommitted_changes[:5]:
            report.append(f"    {change['status']} {change['file']}")
    report.append("")
    
    # SECTION 2: PROD BUILD STATUS
    report.append("🚀 PRODUCTION BUILD STATUS")
    report.append("-" * 80)
    report.append(f"Location: {prod_state.repo_path}")
    report.append(f"Current Branch: {prod_state.current_branch}")
    report.append(f"Uncommitted Changes: {len(prod_state.uncommitted_changes)}")
    report.append(f"Untracked Files: {len(prod_state.untracked_files)}")
    report.append(f"Stale Branches (>30 days): {len(prod_state.stale_branches)}")
    report.append("")
    
    if prod_state.uncommitted_changes:
        report.append("  Uncommitted Changes (⚠️ CRITICAL in production):")
        for change in prod_state.uncommitted_changes:
            report.append(f"    {change['status']} {change['file']}")
    report.append("")
    
    # SECTION 3: BRANCH MANAGEMENT ISSUES
    report.append("🌿 BRANCH MANAGEMENT ANALYSIS")
    report.append("-" * 80)
    
    report.append(f"Dev Build: {len(dev_state.branches)} branches total")
    report.append(f"  - Active branches: {sum(1 for _, b in dev_state.branches.items() if b.get('current') or 'origin' in _)}")
    report.append(f"  - Stale branches: {len(dev_state.stale_branches)}")
    
    if dev_state.stale_branches:
        report.append("    Stale Dev Branches:")
        for branch in dev_state.stale_branches[:5]:
            report.append(f"      • {branch['name']:<30} ({branch['days_old']} days old)")
    
    report.append("")
    report.append(f"Prod Build: {len(prod_state.branches)} branches total")
    report.append(f"  - Active branches: {sum(1 for _, b in prod_state.branches.items() if b.get('current') or 'origin' in _)}")
    report.append(f"  - Stale branches: {len(prod_state.stale_branches)}")
    
    if prod_state.stale_branches:
        report.append("    Stale Prod Branches:")
        for branch in prod_state.stale_branches[:5]:
            report.append(f"      • {branch['name']:<30} ({branch['days_old']} days old)")
    
    report.append("")
    
    # SECTION 4: CRITICAL ISSUES
    report.append("🚨 CRITICAL ISSUES DETECTED")
    report.append("-" * 80)
    
    issues = []
    
    # Issue 1: Uncommitted prod changes
    if len(prod_state.uncommitted_changes) > 0:
        issues.append(
            f"⚠️  PRODUCTION UNCOMMITTED CHANGES: {len(prod_state.uncommitted_changes)} files modified\n"
            f"    This breaks reproducibility and makes rollbacks difficult.\n"
            f"    Files: {', '.join(c['file'] for c in prod_state.uncommitted_changes[:3])}"
        )
    
    # Issue 2: Multiple branches
    total_branches = len(dev_state.branches) + len(prod_state.branches)
    if total_branches > 10:
        issues.append(
            f"🌿 BRANCH SPRAWL: {total_branches} total branches across both builds\n"
            f"    Dead branches create confusion and testing overhead."
        )
    
    # Issue 3: Stale branches
    total_stale = len(dev_state.stale_branches) + len(prod_state.stale_branches)
    if total_stale > 5:
        issues.append(
            f"⏳ STALE BRANCHES: {total_stale} branches older than 30 days\n"
            f"    These should be archived or deleted."
        )
    
    # Issue 4: Dev-Prod divergence
    if "origin/dev" in dev_state.branches and "origin/prod" in prod_state.branches:
        dev_commit = dev_state.branches.get("dev", {}).get("commit", "?")
        prod_commit = prod_state.branches.get("prod", {}).get("commit", "?")
        if dev_commit != prod_commit:
            issues.append(
                f"🔀 DEV-PROD DIVERGENCE: dev and prod branches are separate lineages\n"
                f"    Dev:  {dev_commit}\n"
                f"    Prod: {prod_commit}\n"
                f"    This prevents simple forward-merges. Need a formal promotion path."
            )
    
    # Issue 5: Docker conflict
    issues.append(
        "🐳 DOCKER ISOLATION PROBLEM: Running prod containers blocks dev testing\n"
        f"    Dev path:  {dev_state.repo_path}\n"
        f"    Prod path: {prod_state.repo_path}\n"
        f"    Solution: Use separate compose files with different container names/ports"
    )
    
    for i, issue in enumerate(issues, 1):
        report.append(f"{i}. {issue}")
        report.append("")
    
    return "\n".join(report)


def generate_recommendations(dev_state: WorkflowState, prod_state: WorkflowState) -> str:
    """Generate detailed workflow improvement recommendations"""
    
    recommendations = []
    recommendations.append("=" * 80)
    recommendations.append("WORKFLOW IMPROVEMENT RECOMMENDATIONS")
    recommendations.append("=" * 80)
    recommendations.append("")
    
    recommendations.append("🎯 RECOMMENDED WORKFLOW ARCHITECTURE")
    recommendations.append("-" * 80)
    recommendations.append("""
Primary Branches (Protected):
  • main         - Release-ready code (stable, tagged)
  • staging      - Pre-production testing environment
  • prod         - Current production deployment

Development Branches:
  • dev          - Integration branch for features
  • feature/*    - Individual feature branches (short-lived)

Supporting Infrastructure:
  • docker-compose.yml       - Local dev environment (ports 8080, 5432, etc.)
  • docker-compose.staging.yml - Staging environment (separate ports/containers)
  • docker-compose.prod.yml  - Production environment (separate instance)
""")
    
    recommendations.append("\n📋 IMMEDIATE ACTIONS (This Week)")
    recommendations.append("-" * 80)
    recommendations.append("""
1. COMMIT PRODUCTION CHANGES ✅ URGENT
   $ cd /home/clay/Projects/TheAgame
   $ git add config/nginx/conf.d/app.conf docker-compose.prod.yml
   $ git commit -m "chore: update nginx config and docker-compose for prod deployment"
   $ git push origin prod
   
   Reason: Uncommitted prod changes break reproducibility and disaster recovery.

2. CLEAN UP STALE BRANCHES
   Branches to delete (>30 days old):
   $ cd /home/clay/Development/TheAgame
   $ git branch -d [stale_branch_name]
   $ git push origin --delete [stale_branch_name]
   
   Keep: dev, main, master, staging
   Delete: debug/videoFlow, fallBack, ftanon, devProd, dev2, newDev, prodReady

3. STANDARDIZE COMMIT MESSAGES
   Current: "fixed it", "mmove to WSL2", "gs", "het"
   Desired: "feat: add auth", "fix: handle null pointer", "docs: add guide"
   
   Use: <type>(<scope>): <subject>
   Types: feat, fix, docs, style, refactor, test, chore

4. SET UP .gitignore FOR RUNTIME FILES
   Add to .gitignore:
   - log/*/
   - data/mosquitto_prod/data/
   - data/certbot/
   - .idea/
   - *.log
""")
    
    recommendations.append("\n🏗️ MEDIUM-TERM IMPROVEMENTS (Next 2-4 Weeks)")
    recommendations.append("-" * 80)
    recommendations.append("""
1. IMPLEMENT GIT WORKFLOW (Git Flow)
   
   a) Feature Development:
      $ git checkout -b feature/myfeature dev
      $ # make changes, commit
      $ git push origin feature/myfeature
      $ # Create PR → code review → merge to dev
   
   b) Release to Staging:
      $ git checkout staging
      $ git merge --no-ff dev  # or cherry-pick specific features
      $ git tag -a v1.2.0-rc1
      $ git push origin staging --tags
   
   c) Release to Production:
      $ git checkout prod
      $ git merge --no-ff staging
      $ git tag -a v1.2.0
      $ git push origin prod --tags
   
   Benefits: 
   - Clear promotion path (feature → dev → staging → prod)
   - Easy rollbacks (checkout previous tag)
   - Multiple parallel releases if needed

2. SEPARATE DOCKER COMPOSE FILES
   
   Instead of having prod containers block dev work:
   
   Development (local machine):
   └─ docker-compose.yml (ports 8080-8089, container prefix: "dev_")
   
   Staging (separate environment or machine):
   └─ docker-compose.staging.yml (ports 9080-9089, container prefix: "staging_")
   
   Production (production server):
   └─ docker-compose.prod.yml (ports 80/443, container prefix: "prod_")
   
   This allows:
   ✓ Run dev locally without stopping prod
   ✓ Test staging changes in parallel
   ✓ Hot-swap between branches instantly
   
   Create separate env files:
   - .env.local (dev settings, localhost connections)
   - .env.staging (staging settings, staging credentials)
   - .env.prod (production settings, prod credentials)

3. ADD GITHUB ACTIONS CI/CD
   
   .github/workflows/test.yml:
   - Run tests on every PR and push to dev
   - Build and tag Docker images
   - Run linting and security checks
   
   .github/workflows/deploy-staging.yml:
   - Deploy to staging when PR merged to staging
   - Run smoke tests
   - Alert on deployment failure
   
   .github/workflows/deploy-prod.yml:
   - Deploy to prod on tag (manual trigger)
   - Run health checks
   - Send deployment notification

4. CREATE ISSUE/PR TEMPLATES
   - Link commits to issues
   - Enforce standard PR descriptions
   - Require passing checks before merge
   - Require code reviews for prod branch
""")
    
    recommendations.append("\n🔐 PROCESS IMPROVEMENTS")
    recommendations.append("-" * 80)
    recommendations.append("""
1. BRANCH PROTECTION RULES (GitHub)
   
   Main branches (main, staging, prod):
   ✓ Require pull request review (2 reviewers for prod)
   ✓ Require status checks to pass (CI/CD)
   ✓ Dismiss stale review approvals
   ✓ Restrict who can push to branch
   ✓ Block all committing directly (force PR workflow)

2. RELEASE TAGGING CONVENTION
   
   Prod releases:
   - v1.0.0         (stable release)
   - v1.0.0-rc1     (release candidate for staging)
   - v1.0.0-beta.1  (beta for testing)
   
   This enables:
   - Quick rollback: git checkout v1.0.0
   - Release notes auto-generation
   - Docker image tagging: app:v1.0.0

3. DEPLOYMENT CHECKLIST AUTOMATION
   
   Before prod deployment, ensure:
   ☐ All tests pass
   ☐ Code reviewed and approved
   ☐ Database migrations tested
   ☐ Configuration secrets validated
   ☐ Backup taken
   ☐ Rollback plan documented
   
   Use GitHub Actions to enforce this.

4. COMMIT MESSAGE STANDARDS
   
   Bad:
     - "fixed it"
     - "updates"
     - "mmove to WSL2"
   
   Good:
     - "feat(auth): add JWT token refresh mechanism"
     - "fix(api): handle empty response from MQTT broker"
     - "docs(deploy): update production deployment guide"
     - "chore(docker): update base image to Python 3.12.1"
""")
    
    recommendations.append("\n🚀 DOCKER CONTAINER STRATEGY")
    recommendations.append("-" * 80)
    recommendations.append("""
CURRENT PROBLEM:
  Location: Both in /home/clay/Development/teamAlpha/docker-compose.yml
  Issue: Shared ports and container names conflict between dev/prod
  Impact: Must stop prod containers to test dev changes

PROPOSED SOLUTION:
  
  1. Create docker-compose.dev.yml in /home/clay/Development/teamAlpha/
     ```yaml
     services:
       ollama-dev:
         image: ollama/ollama:latest
         container_name: dev_ollama
         ports:
           - "11434:11434"
         volumes:
           - ollama_dev:/root/.ollama
       
       teamalpha-agent-dev:
         image: teamalpha:dev
         container_name: dev_agent
         ports:
           - "8080:8000"
         environment:
           OLLAMA_HOST: http://dev_ollama:11434
     ```
  
  2. Keep docker-compose.prod.yml separate in /home/clay/Projects/TheAgame/
     ```yaml
     services:
       # ... (unchanged, prod containers)
     ```
  
  3. Usage:
     # Dev testing (doesn't affect prod):
     $ cd /home/clay/Development/teamAlpha
     $ docker compose -f docker-compose.dev.yml up
     
     # Prod stays running independently:
     $ cd /home/clay/Projects/TheAgame
     $ docker compose -f docker-compose.prod.yml up -d
     
     # Test both simultaneously!

BENEFITS:
  ✓ No port conflicts
  ✓ Different container names (dev_* vs prod_*)
  ✓ Different volumes
  ✓ Different env variables
  ✓ Independent lifecycle management
  ✓ Easy to test feature before pushing to prod
""")
    
    recommendations.append("\n📊 WORKFLOW DECISION MATRIX")
    recommendations.append("-" * 80)
    recommendations.append("""
Scenario: What should I do?

1. FIXING A BUG IN PRODUCTION
   ├─ Branch: git checkout -b hotfix/critical-bug prod
   ├─ Fix code in aBackend, gameUI, etc.
   ├─ Test locally: docker compose -f docker-compose.dev.yml up
   ├─ Push: git push origin hotfix/critical-bug
   ├─ PR: Create PR from hotfix → prod (bypass staging)
   ├─ Merge: Merge directly to prod after review
   └─ Deploy: git checkout prod && git pull && docker compose pull && docker compose up -d

2. ADDING A NEW FEATURE
   ├─ Branch: git checkout -b feature/new-feature dev
   ├─ Develop: Make changes, commit frequently
   ├─ Test: docker compose -f docker-compose.dev.yml up
   ├─ Push: git push origin feature/new-feature
   ├─ PR: Create PR from feature → dev
   ├─ Review: Code review by team members
   ├─ Merge: Merge to dev after approval
   ├─ Staging: Wait for release cycle (maybe feature/new-feature → staging → prod)
   └─ Production: After validation in staging

3. TESTING A CHANGE BEFORE PRODUCTION
   ├─ Checkout: git checkout -b test/feature-name staging
   ├─ Cherry-pick: git cherry-pick feature/feature-name
   ├─ Docker: docker compose -f docker-compose.staging.yml up
   ├─ Test: Verify in staging container
   ├─ Decide: Keep it or drop it
   ├─ Deploy: If good, merge to prod
   └─ Production: Deploy via release tag

4. EMERGENCY ROLLBACK
   ├─ Get tag: git tag | grep v
   ├─ Checkout: git checkout v1.0.0
   ├─ Docker: docker compose pull && docker compose up -d
   ├─ Verify: Check health: curl http://localhost/health
   └─ Follow up: Git bisect to find the issue
""")
    
    recommendations.append("\n✅ SUCCESS METRICS")
    recommendations.append("-" * 80)
    recommendations.append("""
Once this workflow is implemented, you should see:

1. Clean git history
   - All commits follow <type>(<scope>): <subject>
   - No more "fixed it", "gs", "het" commits
   - Atomic commits (one feature/fix per commit)

2. Faster deployments
   - Feature to prod: 1-2 days (review cycle)
   - Hotfix to prod: 1-2 hours
   - Rollback: 5 minutes (just checkout tag)

3. Better testing
   - Can test multiple branches in parallel
   - No conflicts with prod running
   - Staging closely mirrors production

4. Easier debugging
   - Clear which commit broke production
   - Easy to bisect between tags
   - Release notes auto-generated from commits

5. Team collaboration
   - Clear who did what and when
   - Easy code review on feature branches
   - No accidental pushes to wrong branch
""")
    
    return "\n".join(recommendations)


def main():
    """Main analysis execution"""
    print("🔍 Analyzing development and production workflows...")
    print()
    
    # Analyze both builds
    dev_state = analyze_workflow(DEV_PATH)
    prod_state = analyze_workflow(PROD_PATH)
    
    # Generate report
    report = generate_workflow_report(dev_state, prod_state)
    print(report)
    
    # Generate recommendations
    recommendations = generate_recommendations(dev_state, prod_state)
    print("\n" + recommendations)
    
    # Save to file
    timestamp = subprocess.run(
        "date +%Y%m%d_%H%M%S",
        shell=True,
        capture_output=True,
        text=True
    ).stdout.strip()
    
    output_file = f"/home/clay/Development/teamAlpha/WORKFLOW_ANALYSIS_{timestamp}.md"
    with open(output_file, "w") as f:
        f.write(report)
        f.write("\n\n")
        f.write(recommendations)
    
    print(f"\n📄 Full report saved to: {output_file}")


if __name__ == "__main__":
    main()
