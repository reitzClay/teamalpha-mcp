# Running Dev, Staging and Prod in Parallel

This document explains how to run development and production stacks simultaneously
on the same machine without port or container name conflicts.

Files added:
- `docker-compose.dev.yml` — development compose (services prefixed with `dev_`)
- `docker-compose.staging.yml` — staging compose scaffold (services prefixed with `staging_`)

Basic usage examples (copy-paste):

1) Start production (if not already running):

```bash
cd /home/clay/Projects/TheAgame
# Start prod in detached mode
docker compose -f docker-compose.prod.yml up -d
```

2) Start development stack (won't interfere with prod):

```bash
cd /home/clay/Development/teamAlpha
docker compose -f docker-compose.dev.yml up --build
```

This maps dev Ollama to host `11435` and the dev agent to host `18080`.

3) Start staging (if needed):

```bash
cd /home/clay/Development/teamAlpha
docker compose -f docker-compose.staging.yml up --build
```

This maps staging Ollama to host `11436` and the staging agent to host `19090`.

Notes:
- Each compose uses different `container_name` prefixes to avoid name conflicts.
- Each compose maps the model server port (`11434`) to a different host port.
- Ensure volumes point to the correct dev/staging/prod paths.
- Use separate `.env` files for dev/staging/prod to keep credentials isolated.

Example stop commands:

```bash
# Stop only dev stack
docker compose -f /home/clay/Development/teamAlpha/docker-compose.dev.yml down

# Stop production (on prod path)
docker compose -f /home/clay/Projects/TheAgame/docker-compose.prod.yml down
```

Advanced:
- If you use systemd or a process manager for prod, keep prod running there and
  use the dev compose for iterative local development.
- Consider using Docker contexts or separate user namespaces for stronger isolation.
