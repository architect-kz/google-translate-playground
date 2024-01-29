#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 [development | production | test | stop]"
  exit 1
fi

# Determine which mode to run
if [ "$1" == "development" ]; then
  COMPOSE_COMMAND="--env-file .env.development up --build -d"
elif [ "$1" == "production" ]; then
  COMPOSE_COMMAND="--env-file .env.production up --build -d"
elif [ "$1" == "test" ]; then
  COMPOSE_COMMAND="-f docker/docker-compose.override.yaml --env-file .env.development up --build tester && docker compose down --remove-orphans"
elif [ "$1" == "stop" ]; then
  eval "docker compose -f docker/docker-compose.yaml down"
  exit 0
else
  echo "Invalid mode. Use 'development', 'production', 'test', or 'stop'"
  exit 1
fi

eval "docker compose -f docker/docker-compose.yaml $COMPOSE_COMMAND"
