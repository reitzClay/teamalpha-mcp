# Getting Started with TeamAlpha

Welcome to TeamAlpha! This guide will get you up and running in minutes.

## ⚡ 30-Second Quick Start

```bash
# Create a new project
python3 quickstart.py --name my-project

# Configure your team
cd projects/my-project
nano team.yaml

# Run it
python3 run.py
```

Done! Your first TeamAlpha project is running.

---

## 📖 Choose Your Learning Path

### 🎯 Path 1: I Want to Build a Project (Recommended)
**Time: 15 minutes**

1. Read: `RESTRUCTURING_COMPLETE.md` (5 min)
2. Create: `python3 quickstart.py --name api-service` (1 min)
3. Configure: Edit `team.yaml` and `project.yaml` (5 min)
4. Run: `python3 run.py` (1 min)
5. Review: Check output in `output/` folder (3 min)

### 🔬 Path 2: I Want to Understand the Framework
**Time: 30 minutes**

1. Read: `docs/TEAM_GUIDE.md` (15 min)
2. Read: `STRUCTURE_GUIDE.md` (10 min)
3. Study: `src/teamalpha/agent.py` (5 min)

### 🐳 Path 3: I Want to Set Up Infrastructure
**Time: 20 minutes**

1. Read: `docs/DEV_RUN.md` (5 min)
2. Start dev: `cd infrastructure && docker compose -f docker-compose.dev.yml up` (2 min)
3. Start staging: `cd infrastructure && docker compose -f docker-compose.staging.yml up` (2 min)
4. Test: Access both environments (5 min)
5. Review: Check compose files (5 min)

### 📚 Path 4: I Want to Study Examples
**Time: 25 minutes**

1. Read: `RESTRUCTURING_COMPLETE.md` (5 min)
2. Run: `python3 examples/example_team.py` (5 min)
3. Study: `examples/example_team.py` code (10 min)
4. Run: `python3 examples/run_team_on_prod.py` (5 min)

---

## 🚀 Common Tasks

### Create a New Project
```bash
python3 quickstart.py --name my-awesome-project
cd projects/my-awesome-project
nano team.yaml          # Define your team
python3 run.py          # Run the project
```

### View All Documentation
```bash
ls -la docs/
ls -la projects/greenfield-starter/
```

### Run Development Environment
```bash
cd infrastructure
docker compose -f docker-compose.dev.yml up --build
```

### Analyze a Repository
```bash
python3 tools/workflow_analyzer.py
```

### Study Framework Code
```bash
cat src/teamalpha/agent.py      # Agent base class
cat src/teamalpha/team.py       # Team orchestration
cat src/teamalpha/client.py     # HTTP client
```

---

## 📁 Key Files to Know

| File | Purpose |
|------|---------|
| `quickstart.py` | Create new projects |
| `INDEX.md` | Navigation guide |
| `RESTRUCTURING_COMPLETE.md` | What changed |
| `STRUCTURE_GUIDE.md` | Directory structure explained |
| `docs/TEAM_GUIDE.md` | Framework documentation |
| `docs/DEV_RUN.md` | How to run dev/prod parallel |
| `projects/greenfield-starter/` | Template for new projects |
| `examples/example_team.py` | Working example |
| `infrastructure/docker-compose.dev.yml` | Development setup |

---

## ✅ Checklist for First Project

- [ ] Read `RESTRUCTURING_COMPLETE.md` (understand the structure)
- [ ] Run `python3 quickstart.py --name my-project`
- [ ] Edit `projects/my-project/team.yaml` (define your team)
- [ ] Edit `projects/my-project/project.yaml` (update metadata)
- [ ] Run `cd projects/my-project && python3 run.py`
- [ ] Check `projects/my-project/output/` for results
- [ ] Review `docs/TEAM_GUIDE.md` for advanced usage

---

## 🆘 Troubleshooting

### "Module not found" errors
```bash
export PYTHONPATH="${PYTHONPATH}:/home/clay/Development/teamAlpha"
```

### Docker container errors
```bash
docker ps              # Check running containers
docker compose down    # Stop all containers
docker system prune    # Clean up
```

### Project creation fails
```bash
ls projects/           # Verify greenfield-starter exists
python3 quickstart.py --name test-project  # Try again
```

---

## 🎓 What You'll Learn

Using TeamAlpha, you'll learn:

- **Multi-agent collaboration** - How agents work together on tasks
- **LLM-powered decision making** - Using language models for logic
- **Team orchestration** - Managing complex workflows
- **Docker containerization** - Running isolated environments
- **Git workflows** - Professional development practices
- **Project organization** - Scaling development teams

---

## 📞 Getting Help

1. **Quick reference**: `INDEX.md`
2. **Structure**: `STRUCTURE_GUIDE.md`
3. **Framework**: `docs/TEAM_GUIDE.md`
4. **Setup**: `docs/DEV_RUN.md`
5. **Examples**: `examples/`

---

## 🎯 Your First Project

Ready? Let's go:

```bash
# Create
python3 quickstart.py --name hello-world

# Configure
cd projects/hello-world
cat team.yaml

# Run
python3 run.py

# Check results
cat output/report.md
```

That's it! You've successfully run your first TeamAlpha project.

---

## 🚀 What's Next?

1. Create more projects with different team compositions
2. Build custom workflows in `workflows/`
3. Implement tools in `tools/`
4. Integrate with your CI/CD pipeline
5. Deploy using Docker compose files

---

**You're all set! Start building with TeamAlpha!** 🎉

Questions? Check the documentation in `docs/` folder.
