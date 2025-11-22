# TeamAlpha Project Index

**Status**: ✅ Restructured and Ready for Greenfield Development  
**Last Updated**: 2025-11-22  
**Current Branch**: main  
**Commits Ahead**: 12 (ready to push)

---

## 📚 Documentation (Start Here)

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **RESTRUCTURING_COMPLETE.md** | Summary of changes and benefits | 5 min |
| **STRUCTURE_GUIDE.md** | Navigation guide and file organization rationale | 8 min |
| **README_STRUCTURE.md** | Comprehensive structure overview with examples | 10 min |
| **docs/TEAM_GUIDE.md** | Complete framework documentation | 15 min |
| **docs/DEV_RUN.md** | How to run dev and prod in parallel | 5 min |

---

## 🚀 Quick Start Paths

### For Beginners
1. Read: **RESTRUCTURING_COMPLETE.md**
2. Run: `python3 quickstart.py --name my-first-project`
3. Follow: `projects/my-first-project/QUICKSTART.md`

### For Experienced Users
1. Read: **docs/TEAM_GUIDE.md**
2. Clone: `cp -r projects/greenfield-starter projects/my-project`
3. Run: `cd projects/my-project && python3 run.py`

### For DevOps/Infrastructure
1. Read: **docs/DEV_RUN.md**
2. Check: `infrastructure/docker-compose.dev.yml`
3. Deploy: `docker compose -f infrastructure/docker-compose.dev.yml up`

---

## 📁 Directory Structure

```
teamAlpha/
├── src/teamalpha/              Core framework (production)
├── infrastructure/             Docker & deployment configs
├── docs/                       All documentation
├── examples/                   Reference implementations
├── tools/                      Utility scripts
├── projects/                   Project workspaces
│   ├── greenfield-starter/     Template for new projects
│   ├── theagame-analysis/      Completed analysis project
│   └── demo-api-service/       Example created by quickstart
├── quickstart.py               Create new projects
└── README.md                   Main readme
```

---

## 🎯 Common Tasks

### Create a New Project
```bash
python3 quickstart.py --name my-new-project
cd projects/my-new-project
nano team.yaml
python3 run.py
```

### Run Development Environment
```bash
cd infrastructure
docker compose -f docker-compose.dev.yml up --build
```

### View Documentation
```bash
ls docs/
cat docs/TEAM_GUIDE.md
```

---

## 🚀 Ready to Start?

```bash
# Option 1: Create new project
python3 quickstart.py --name my-project

# Option 2: Run dev environment
cd infrastructure && docker compose -f docker-compose.dev.yml up

# Option 3: View documentation
cat RESTRUCTURING_COMPLETE.md
```

---

**TeamAlpha is ready for greenfield development!** ✅
