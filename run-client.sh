#!/bin/bash
# Start the interactive TeamAlpha client with proper environment

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python3"

echo "🚀 TeamAlpha Interactive Client Launcher"
echo ""

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found at $VENV_PYTHON"
    echo "   Run: uv sync"
    exit 1
fi

# Check if containers are running
if ! docker ps 2>/dev/null | grep -q dev_teamalpha_agent; then
    echo "⚠️  Agent container not running"
    echo "   Start with: docker compose -f infrastructure/docker-compose.dev.yml up -d"
    read -p "   Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the client
echo "📡 Starting interactive client..."
echo ""

exec "$VENV_PYTHON" "$PROJECT_ROOT/interactive_client.py"
