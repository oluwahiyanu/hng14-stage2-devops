#!/bin/bash
set -e

echo "Starting integration test..."

# Start stack
docker compose up -d --build

# Wait for services
echo "Waiting for services to be healthy..."
TIMEOUT=60
ELAPSED=0
until [ "$(docker compose ps | grep -c "healthy")" -ge 3 ] || [ $ELAPSED -ge $TIMEOUT ]; do
  sleep 5
  ELAPSED=$((ELAPSED + 5))
  echo "Waiting... ${ELAPSED}s"
done

if [ $ELAPSED -ge $TIMEOUT ]; then
  echo "Timeout waiting for services"
  docker compose down -v
  exit 1
fi

# Submit a job
RESPONSE=$(curl -sf http://localhost:3000/submit \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"task":"integration-test"}')
echo "Submit response: $RESPONSE"

JOB_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

# Poll for completion with timeout
TIMEOUT=60
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
  STATUS=$(curl -sf http://localhost:3000/status/$JOB_ID | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS (${ELAPSED}s)"
  if [ "$STATUS" = "completed" ]; then
    echo "Integration test passed!"
    docker compose down -v
    exit 0
  fi
  sleep 5
  ELAPSED=$((ELAPSED + 5))
done

echo "Integration test timed out"
docker compose down -v
exit 1
