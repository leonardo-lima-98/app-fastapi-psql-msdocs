import multiprocessing

max_requests = 100
max_requests_jitter = 5
log_file = "-"
bind = "0.0.0.0:8000"
# workers = (multiprocessing.cpu_count() * 2) + 1
workers = 4

worker_class = "my_uvicorn_worker.MyUvicornWorker"

timeout = 600
