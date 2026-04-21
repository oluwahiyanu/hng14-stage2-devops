import redis
import time
import os
import signal
import sys

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

running = True
def signal_handler(signum, frame):
    global running
    print("Received shutdown signal, exiting...")
    running = False
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


print("Worker started, waiting for jobs...")
while running:
    try:
        job = r.brpop("job", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id)
    except redis.ConnectionError:
        print("Redis connection lost, retrying in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        print(f"Error processing job: {e}")
