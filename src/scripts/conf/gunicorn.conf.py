import multiprocessing
import os

max_requests = 100
max_requests_jitter = 5
log_file = "-"
bind = "0.0.0.0:8000"

env = os.getenv("ENV")
if env is None:
    workers = (multiprocessing.cpu_count() * 2) + 1
else:
    workers = 2

worker_class = "my_uvicorn_worker.MyUvicornWorker"

timeout = 600

if __name__ == "__main__":
    print(env)