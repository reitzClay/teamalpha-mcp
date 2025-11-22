# Greenfield Project Starter

Use this template to quickly bootstrap a new project with TeamAlpha.

## Quick Start

1. **Copy this directory to a new project name:**
   ```bash
   cp -r greenfield-starter ../my-new-project
   cd ../my-new-project
   ```

2. **Update project metadata** in `project.yaml`:
   ```yaml
   name: my-new-project
   description: "Description of your project"
   ```

3. **Create your team** in `team.yaml`:
   ```yaml
   agents:
     - name: Alice
       role: engineer
     - name: Bob
       role: code_reviewer
   ```

4. **Define workflows** in `workflows/`:
   - Create workflow files (e.g., `api_design.py`, `code_review.py`)
   - Each workflow defines a sequence of tasks

5. **Register tools** in `tools.yaml`:
   - Map tool names to their implementations
   - Tools are Python callables that agents can invoke

6. **Run the project**:
   ```bash
   python3 run.py
   ```

## Project Structure

```
my-new-project/
├── README.md                 # This file
├── project.yaml              # Project metadata
├── team.yaml                 # Team definition
├── tools.yaml                # Tool registry
├── run.py                    # Main entry point
├── workflows/                # Workflow definitions
│   ├── __init__.py
│   └── api_design.py
├── tools/                    # Custom tool implementations
│   ├── __init__.py
│   └── code_analyzer.py
└── output/                   # Generated outputs (reports, etc.)
    └── .gitkeep
```

## Example Workflow

See `workflows/api_design.py` for a complete example of:
- Creating a team
- Defining a workflow
- Executing tasks
- Collecting and reporting results

## Configuration Files

### project.yaml
Metadata about your project:
```yaml
name: api-service
version: 1.0.0
description: "REST API for user management"
tags:
  - backend
  - api
```

### team.yaml
Define team members and their roles:
```yaml
agents:
  - name: Alice
    role: engineer
    description: "Backend engineer"
  - name: Bob
    role: code_reviewer
    description: "Code quality expert"
  - name: Eve
    role: architect
    description: "System design specialist"
```

### tools.yaml
Register custom tools:
```yaml
tools:
  - name: code_analyzer
    description: "Analyze code quality"
    module: tools.code_analyzer
    function: analyze_code
  
  - name: api_generator
    description: "Generate API stubs"
    module: tools.api_generator
    function: generate_api
```

## Running Workflows

### Interactive Execution
```bash
# Run with live output
python3 run.py --workflow api_design --verbose
```

### Generate Report
```bash
# Run and save to markdown
python3 run.py --workflow api_design --report output/report.md
```

### Batch Execution
```bash
# Run multiple workflows
python3 run.py --workflows api_design,code_review --parallel
```

## Extending

### Add a Custom Tool
1. Create `tools/my_tool.py`:
   ```python
   def my_tool(input_data: str) -> str:
       return f"Processed: {input_data}"
   ```

2. Register in `tools.yaml`:
   ```yaml
   - name: my_tool
     module: tools.my_tool
     function: my_tool
   ```

3. Use in a workflow:
   ```python
   result = agent.execute("[TOOL: my_tool, ARGS: {'input_data': 'data'}]")
   ```

### Add a New Workflow
1. Create `workflows/my_workflow.py`
2. Define tasks and assign to agents
3. Execute and save results

### Add Team Members
Edit `team.yaml` and restart the project.

## Troubleshooting

**LLM Connection Error**: Ensure Ollama is running on `http://ollama:11434`
**Tool Not Found**: Check that tool is registered in `tools.yaml`
**Agent Not Found**: Verify agent name matches in `team.yaml`

## Next Steps

- Define your team in `team.yaml`
- Implement your workflows in `workflows/`
- Create custom tools in `tools/`
- Run `python3 run.py` to execute

For more details, see `docs/TEAM_GUIDE.md` in the main TeamAlpha directory.
