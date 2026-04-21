# Bug Fixes Documentation

## Fix 1
- **File:** `api/main.py`
- **Line:** 6
- **Problem:** Redis host hardcoded as `"localhost"` — fails inside Docker network
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 2
- **File:** `api/main.py`
- **Line:** 6
- **Problem:** Redis port hardcoded as `6379`
- **Fix:** Changed to `int(os.getenv("REDIS_PORT", 6379))`

## Fix 3
- **File:** `api/main.py`
- **Line:** 6
- **Problem:** Missing `decode_responses=True` — requires manual `.decode()`
- **Fix:** Added `decode_responses=True` to Redis client

## Fix 4
- **File:** `api/main.py`
- **Line:** 18
- **Problem:** `status.decode()` fails when `decode_responses=True` is used
- **Fix:** Removed `.decode()` call

## Fix 5
- **File:** `api/main.py`
- **Line:** 10-18
- **Problem:** Missing `/health` endpoint — required for Docker HEALTHCHECK
- **Fix:** Added `@app.get("/health")` endpoint

## Fix 6
- **File:** `worker/worker.py`
- **Line:** 5
- **Problem:** Redis host hardcoded as `"localhost"`
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 7
- **File:** `worker/worker.py`
- **Line:** 5
- **Problem:** Redis port hardcoded as `6379`
- **Fix:** Changed to `int(os.getenv("REDIS_PORT", 6379))`

## Fix 8
- **File:** `worker/worker.py`
- **Line:** 15
- **Problem:** `job_id.decode()` fails with `decode_responses=True`
- **Fix:** Removed `.decode()` call

## Fix 9
- **File:** `worker/worker.py`
- **Line:** 5
- **Problem:** Missing `decode_responses=True`
- **Fix:** Added `decode_responses=True` to Redis client

## Fix 10
- **File:** `worker/worker.py`
- **Line:** 18-20
- **Problem:** No graceful shutdown mechanism
- **Fix:** Added signal handlers for SIGTERM/SIGINT

## Fix 11
- **File:** `frontend/app.js`
- **Line:** 6
- **Problem:** API URL hardcoded as `"http://localhost:8000"`
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Fix 12
- **File:** `api/.env`
- **Line:** N/A
- **Problem:** `.env` file committed to git repository — security risk
- **Fix:** Removed from git, added to `.gitignore`, created `.env.example`

## Fix 13
- **File:** `worker/requirements.txt`
- **Line:** 4
- **Problem:** Duplicate `redis` entry
- **Fix:** Removed duplicate

## Fix 14
- **File:** `api/main.py`
- **Line:** 12-18
- **Problem:** No error handling for Redis connection failures
- **Fix:** Added try/except with HTTP 503 responses

## Fix 15
- **File:** `frontend/app.js`
- **Line:** 13, 22
- **Problem:** Generic error messages with no debugging info
- **Fix:** Enhanced error responses with actual error details

## Fix 16
- **File:** `frontend/Dockerfile`
- **Problem:** `npm ci` failed because `package-lock.json` was missing from the repository.
- **Fix:** Switched to `npm install --omit=dev` to allow building without a lockfile while still excluding development dependencies. 
