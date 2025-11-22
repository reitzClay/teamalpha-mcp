# TeamAlpha Restructured - Project Organization Guide

## New Directory Structure

```
teamAlpha/
│
├── README.md                          ← Main project readme (update this)
├── README_STRUCTURE.md                ← Complete structure guide (this file in root)
├── pyproject.toml                     ← Python dependencies
├── Dockerfile                         ← Container image
├── server.py                          ← FastAPI HTTP wrapper
├── client.py                          ← CLI client
│
├── 📁 src/teamalpha/                  ← Core framework (PRODUCTION CODE)
│   ├── __init__.py
│   ├── agent.py                       ← Agent base class & roles
│   ├── team.py                        ← Team orchestration
│   ├── client.py                      ← HTTP client library
│   ├── config/
│   │   └── tasks.yaml
│   └── tools/
│       └── __init__.py
│
├── 📁 infrastructure/                 ← Docker & deployment
│   ├── docker-compose.yml             ← Current compose (legacy)
│   ├── docker-compose.dev.yml         ← Development (isolated ports)
│   └── docker-compose.staging.yml     ← Staging template
│
├── 📁 docs/                           ← Documentation
│   ├── TEAM_GUIDE.md                  ← Framework guide
│   ├── DEV_RUN.md                     ← How to run dev/prod in parallel
│   ├── MCP_ARCHITECTURE.md
│   ├── MCP_INTEGRATION_GUIDE.md
│   ├── MCP_QUICK_REFERENCE.md
│   ├── MCP_SUMMARY.md
│   └── (more guides)
│
├── 📁 examples/                       ← Reference implementations
│   ├── example_team.py                ← Team collaboration demo
│   └── run_team_on_prod.py            ← Run agents on real repo
│
├── 📁 tools/                          ← Utility tools & scripts
│   ├── workflow_analyzer.py           ← Git workflow analyzer
│   ├── mcp_tool_demo.py               ← MCP demonstrations
│   └── mcp_executor_agent.py          ← MCP executor
│
├── 📁 projects/                       ← Project workspaces
│   │
│   ├── theagame-analysis/             ← TheAgame project (COMPLETED)
│   │   ├── analyze_theagame.py        ← Dev build analysis
│   │   ├── analyze_theagame_prod.py   ← Prod build analysis
│   │   ├── THEAGAME_ANALYSIS.md       ← Dev documentation
│   │   ├── THEAGAME_PROD_ANALYSIS.md  ← Prod documentation
│   │   └── TEAM_RUN_REPORT_*.md       ← Agent execution reports
│   │
│   └── greenfield-starter/            ← NEW PROJECT TEMPLATE ✨
│       ├── README.md                  ← Getting started guide
│       ├── project.yaml               ← Project metadata
│       ├── team.yaml                  ← Team definition
│       ├── tools.yaml                 ← Tool registry
│       ├── run.py                     ← Main entry point
│       ├── workflows/
│       │   └── __init__.py            ← Workflow definitions
│       ├── tools/
│       │   └── __init__.py            ← Custom tools
│       └── output/
│           └── .gitkeep               ← Generated reports
│
└── 📁 config/                         ← Configuration templates
    ├── agents.yaml
    └── tasks.yaml
```

## Navigation Guide

### For Framework Development
```
Core Code:           src/teamalpha/
Tests:               (add to src/tests/)
Documentation:       docs/
```

### For Using the Framework
```
Quick Start:         docs/DEV_RUN.md
API Reference:       docs/TEAM_GUIDE.md
Examples:            examples/
```

### For Project Work
```
New Project:         cp -r projects/greenfield-starter projects/my-project
Analysis Tools:      tools/
Project Reports:     projects/your-project/output/
```

### For Deployment
```
Development:         infrastructure/docker-compose.dev.yml
Staging:             infrastructure/docker-compose.staging.yml
Production:          (separate prod repo)
```

## Key Improvements

✅ **Separation of Concerns**
- Core framework isolated in `src/teamalpha/`
- Projects in `projects/` (isolated per-project)
- Tools and utilities in separate folders

✅ **Easy Navigation**
- Documentation centralized in `docs/`
- Examples show usage patterns
- Infrastructure configs in one place

✅ **Scalability**
- Multiple projects can coexist
- Each project has its own team/workflow/tools
- Can easily add new projects

✅ **Greenfield Support**
- Copy `projects/greenfield-starter/` to start new project
- Pre-configured YAML files
- Ready-to-run template

## Common Tasks

### Create a New Project
```bash
cp -r projects/greenfield-starter projects/my-new-project
cd projects/my-new-project
nano project.yaml    # Edit metadata
nano team.yaml       # Define team
python3 run.py
```

### Run Development Stack
```bash
cd infrastructure
docker compose -f docker-compose.dev.yml up --build
```

### Run Analysis Tool
```bash
python3 tools/workflow_analyzer.py
```

### View Documentation
```bash
ls docs/             # Browse all guides
cat docs/TEAM_GUIDE.md
```

### Run Example
```bash
python3 examples/example_team.py
```

## File Organization Rationale

### `src/teamalpha/` (Stable, Production)
- Core framework classes
- Unlikely to change frequently
- Can be packaged as library

### `projects/` (Mutable, User-Driven)
- Per-project configurations
- Project-specific tools
- Generated outputs
- Easy to add/remove projects

### `tools/` (Utilities)
- Standalone scripts
- Analysis and helpers
- Can be run independently

### `infrastructure/` (Deployment)
- Docker configs
- Environment-specific setups
- Version-controlled deployments

### `docs/` (Knowledge)
- User guides
- API documentation
- Architecture explanations
- Integration guides

### `examples/` (Learning)
- Reference implementations
- Runnable demos
- Best practices

## Migration Notes

**What Changed:**
- Old loose `.py` files moved to organized folders
- Docker files in `infrastructure/`
- Analysis scripts in `projects/theagame-analysis/`

**What Stayed the Same:**
- `src/teamalpha/` - core framework (unchanged)
- `pyproject.toml`, `Dockerfile` - same location
- `server.py`, `client.py` - same location

**Backwards Compatibility:**
- All imports still work (relative paths adjusted)
- Existing workflows/examples still functional
- Git history preserved via git mv

## Next Steps

1. **Push to GitHub**: `git push origin main`
2. **Document project**: Update main `README.md`
3. **Start greenfield project**: Use template in `projects/greenfield-starter/`
4. **Add team tasks**: Edit `team.yaml` for your project
5. **Run workflows**: `python3 projects/your-project/run.py`

## Questions?

- See `docs/TEAM_GUIDE.md` for framework details
- Check `examples/` for reference implementations
- Review `projects/greenfield-starter/README.md` for new project setup
