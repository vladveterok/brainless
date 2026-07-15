#!/usr/bin/env bash
set -e

echo "Starting host environment setup for Universal Second Brain Ingester..."

# 1. Check for required dependencies
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker."
    exit 1
fi

if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "Error: Docker Compose V2 is not installed or not active. V1 is deprecated and unsupported."
    echo "Please run: sudo apt remove docker-compose -y && sudo apt install docker-compose-v2 -y"
    exit 1
fi

# 2. Setup environment variables
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please update the .env file with your actual secrets (especially TELEGRAM_BOT_TOKEN) before starting n8n."
else
    echo ".env file already exists."
fi

# 3. Validate essential environment variables
echo "Validating environment variables..."
source .env

REQUIRED_VARS=("TELEGRAM_BOT_TOKEN")
MISSING_VARS=0

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ] || [ "${!var}" == "your_telegram_bot_token_here" ]; then
        echo "Warning: Required environment variable $var is not properly set in .env"
        MISSING_VARS=$((MISSING_VARS+1))
    fi
done

if [ $MISSING_VARS -gt 0 ]; then
    echo "--------------------------------------------------------"
    echo "Setup requires your attention."
    echo "Please fill in the missing variables in .env."
    echo "Then you can start the environment manually using:"
    echo "./scripts/setup_host.sh"
    echo "--------------------------------------------------------"
    exit 1
fi

echo "Environment validated successfully!"

# 4. Start n8n
echo "Starting n8n via Docker Compose..."
$DOCKER_COMPOSE_CMD up -d --build --force-recreate

echo "--------------------------------------------------------"
echo "n8n is running. You can access it at http://localhost:5678"
echo "Next step: Open n8n, create an account, and configure the Telegram Trigger node."
echo "--------------------------------------------------------"
