# TheAgame Repository Analysis

## Overview

**TheAgame** is a full-stack multiplayer word game with integrated video chat, built with:
- **Frontend**: Ionic 7+/Angular 17+ (TypeScript)
- **Backend**: Spring Boot 3.x (Java 17+)  
- **Real-time Comms**: LiveKit (WebRTC-based video/audio)
- **DevOps**: Docker Compose, Kubernetes-ready

---

## Project Structure

```
TheAgame/
├── aBackend/                  # Java Spring Boot REST API
│   ├── .mvn/                  # Maven wrapper
│   ├── src/                   # Source code
│   ├── pom.xml                # Maven dependencies
│   ├── Dockerfile             # Container config
│   └── mvnw                   # Maven CLI
│
├── gameUI/                    # Ionic/Angular frontend
│   ├── src/                   # Angular components, services
│   ├── angular.json           # Angular CLI config
│   ├── package.json           # Node.js dependencies
│   └── Dockerfile             # Container config
│
├── livekit-token-service/     # Node.js service for LiveKit tokens
│   ├── src/                   # Express.js app
│   ├── package.json           # Dependencies
│   ├── Dockerfile             # Container config
│   └── .env                   # Environment variables
│
├── config/                    # Configuration files
│   └── livekit/               # LiveKit settings
│
├── docker-compose.yml         # Orchestration (Dev/Prod)
├── README.md                  # Full documentation
└── .github/                   # GitHub Actions (CI/CD)
```

---

## Technology Stack

| Component | Tech | Purpose |
|-----------|------|---------|
| **Frontend** | Ionic 7+, Angular 17+, TypeScript | Responsive UI, game interface |
| **Backend** | Spring Boot 3.x, Java 17+, Maven | REST APIs, game logic, auth |
| **Video/Audio** | LiveKit, WebRTC, Redis | Real-time peer-to-peer comms |
| **Database** | H2 (dev), PostgreSQL (prod) | User data, game state |
| **Deployment** | Docker, Docker Compose, K8s-ready | Containerized, cloud-native |
| **Auth** | Spring Security, JWT | User authentication |

---

## Key Services

### 1. **aBackend** (Spring Boot)
- **Port**: ~8080 (configurable)
- **Endpoints**: 
  - Authentication (login, register)
  - Game operations (create room, join game, play)
  - LiveKit token generation
  - User management
- **Tech**: Spring Web, Spring Data JPA, Spring Security, LiveKit SDK

### 2. **gameUI** (Ionic/Angular)
- **Port**: ~4200 (dev), ~80 (prod via Nginx)
- **Features**:
  - Game lobby
  - Real-time multiplayer word game UI
  - Integrated LiveKit video chat
  - PWA-capable
- **Dependencies**: `livekit-client`, Angular Material, etc.

### 3. **livekit-token-service** (Node.js/Express)
- **Port**: ~3000
- **Purpose**: Generate secure LiveKit tokens for frontend
- **Uses**: `livekit-server-sdk`

### 4. **Database** (PostgreSQL)
- **Port**: 5432
- **Schema**: User accounts, games, room data
- **Migrations**: Likely via Flyway or Liquibase (in aBackend)

### 5. **LiveKit Media Server**
- **Port**: 7880 (signaling), 50000-60000 (RTC media)
- **Purpose**: WebRTC media relay, room management
- **Storage**: Redis coordination

---

## How It Works

### User Flow
1. **Registration**: User signs up via gameUI → Backend validates & creates account
2. **Login**: JWT token issued by Spring Security
3. **Create/Join Game**: User enters game room via frontend
4. **Token Generation**: Backend calls livekit-token-service to generate access token
5. **Video Chat**: Frontend connects to LiveKit using token
6. **Gameplay**: Real-time word game mechanics (shared state via backend)

### Architecture Diagram
```
┌─────────────────┐
│   gameUI        │ (Ionic/Angular frontend)
│  :4200          │
└────────┬────────┘
         │
    ┌────┴──────────────┬────────────────┐
    │                   │                │
┌───▼─────┐      ┌─────▼──┐      ┌──────▼────────┐
│ aBackend│      │livekit │      │ livekit-token │
│:8080    │      │:7880   │      │ -service:3000 │
└───┬─────┘      └────┬───┘      └──────┬────────┘
    │                 │                 │
    └─────────────────┼─────────────────┘
                      │
                ┌─────▼────────┐
                │ PostgreSQL   │
                │ Redis        │
                └──────────────┘
```

---

## Development Setup

### Quick Start (Docker Compose)
```bash
# Clone
git clone <repo-url>
cd TheAgame

# Configure (edit .env, config/livekit/*)
cp .env.example .env

# Run all services
docker-compose up

# Access:
# - Frontend: http://localhost:4200
# - Backend API: http://localhost:8080
# - LiveKit: ws://localhost:7880
```

### Local Development (IDE)
1. **Backend**: 
   ```bash
   cd aBackend
   ./mvnw spring-boot:run
   ```

2. **Frontend**:
   ```bash
   cd gameUI
   npm install
   ng serve --open
   ```

3. **Token Service**:
   ```bash
   cd livekit-token-service
   npm install
   npm start
   ```

---

## Key Configurations

| File | Purpose |
|------|---------|
| `aBackend/application.yml` | Spring Boot config |
| `gameUI/angular.json` | Angular CLI config |
| `docker-compose.yml` | Service orchestration |
| `config/livekit/*` | LiveKit settings (room templates, etc.) |
| `.env` files | Secrets, API keys, hosts |

---

## For TeamAlpha Agent

The agent can:
1. **Inspect Code**: Read Java/TypeScript/JavaScript files to understand logic
2. **Suggest Improvements**: Code quality, architecture, security
3. **Generate Tests**: Unit/integration tests for each service
4. **Optimize Docker**: Reduce image sizes, improve build caching
5. **Document APIs**: Auto-generate OpenAPI/Swagger from Spring endpoints
6. **CI/CD Setup**: Create GitHub Actions workflows
7. **Deploy Config**: Generate Kubernetes manifests
8. **Security Audit**: Check for vulnérabilités, best practices

---

## What Agent Can Do Next

```python
# Example: Agent reads a file from TheAgame
from src.teamalpha.agent import Agent, AgentRole, Tool

def read_file(filepath: str) -> str:
    with open(filepath, 'r') as f:
        return f.read()

agent = Agent("CodeReviewer", AgentRole.REVIEWER)
agent.add_tool(Tool(
    name="read_source",
    description="Read source code files",
    func=read_file,
    required_args=["filepath"]
))

# Analyze a Spring endpoint
result = agent.execute("""
Review this file and suggest improvements:
/home/clay/Development/TheAgame/aBackend/src/main/java/com/game/controller/GameController.java
""")
```

---

## Next Steps for Development

- [ ] Add user authentication tests
- [ ] Implement game state synchronization
- [ ] Optimize video codec selection
- [ ] Add telemetry/monitoring (Prometheus)
- [ ] Create Helm charts for Kubernetes
- [ ] Setup staging/production CI/CD
- [ ] Security audit (OWASP Top 10)
- [ ] Performance testing (load testing with Gatling)
