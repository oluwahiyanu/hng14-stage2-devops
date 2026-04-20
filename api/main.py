from fastapi import FastAPI, HTTPException
import redis
import uuid
import os

app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush("job", job_id)
        r.hset(f"job:{job_id}", mapping={"status": "queued"})
        return {"job_id": job_id}
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis connection failed")

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
        if not status:
            return {"error": "not found"}
        return {"job_id": job_id, "status": status}
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis connection failed")
