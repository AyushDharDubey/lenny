#!/usr/bin/env bash

./docker/configure.sh

# Function to wait for a Docker container to be running
# Arguments:
#   $1: The name of the Docker container to wait for (e.g., "lenny_api")
#   $2: (Optional) Maximum number of attempts (default: 15)
#   $3: (Optional) Sleep duration between attempts in seconds (default: 2)
function wait_for_docker_container() {
    local container_name="${1}"
    local max_attempts="${2:-15}" # Default to 15 attempts if not provided
    local wait_seconds="${3:-2}" # Default to 2 seconds if not provided

    if [[ -z "$container_name" ]]; then
        echo "[!] Error: No container name provided to wait_for_docker_container function."
        return 1 # Indicate failure
    fi

    echo "[+] Waiting up to $((max_attempts * wait_seconds)) seconds for '$container_name' to start and pass health checks..."

    local container_ready=false
    for ((i=1; i<=max_attempts; i++)); do
        if docker ps -f "name=$container_name" -f status=running -q &>/dev/null; then
            echo "[+] '$container_name' service is running."
            container_ready=true
            break # Exit the loop immediately
        fi

        echo "    Attempt $i/$max_attempts: Still waiting for '$container_name'..."
        sleep "$wait_seconds"
    done

    if ! "$container_ready"; then
        echo "[!] Error: '$container_name' did not launch after $((max_attempts * wait_seconds)) seconds."
        return 1 # Indicate failure
    fi

    return 0 # Indicate success
}

MODE=
LOG=
REBUILD=false
PRELOAD=""

# Parse cli args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --rebuild)
      REBUILD=true
      shift
      ;;
    --preload)
      # If next arg exists and is a value (not another flag)
      if [[ -n "$2" && "$2" != --* ]]; then
        PRELOAD="$2"
        shift 2
      else
        PRELOAD=true
        shift
      fi
      ;;
    --dev)
      MODE="dev"
      shift
      ;;
    --log)
      LOG=true
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      shift
      ;;
  esac
done


if [[ "$MODE" == "dev" ]]; then
    echo "Running in development mode..."
    if [ ! -f ./env/bin/activate ]; then
        virtualenv env
    fi
    source ./env/bin/activate
    pip install --index-url --index-url "${PIP_INDEX_URL:-https://pypi.org/simple}" --no-cache-dir -r requirements.txt
    source ./env/bin/activate
    uvicorn lenny.app:app --reload
else
    echo "Running in production mode..."
    export $(grep -v '^#' .env | xargs)

    if [[ "$REBUILD" == "true" ]]; then
        echo "Performing full rebuild..."
        docker compose down --volumes --remove-orphans
        docker compose build --no-cache
        docker compose up -d
    else
        docker-compose -p lenny up -d
    fi

    if [[ -n "$PRELOAD" ]]; then
        if wait_for_docker_container "lenny_api" 15 2; then
            if [[ "$PRELOAD" =~ ^[0-9]+$ ]]; then
                EST_MIN=$(echo "scale=2; (800 / $PRELOAD) / 60" | bc)
                LIMIT="-n $PRELOAD"
            else
                EST_MIN=$(echo "scale=2; 800 / 60" | bc)
                LIMIT=""
            fi

            echo "[+] Preloading ${PRELOAD:-ALL}/~800 book(s) from StandardEbooks (~$EST_MIN minutes)..."
        docker exec -it lenny_api python scripts/preload.py $LIMIT
        fi
    fi

    if [[ "$LOG" == "true" ]]; then
        docker compose logs -f
    fi
fi
