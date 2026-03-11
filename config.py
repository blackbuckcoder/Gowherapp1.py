import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"  # Matches your Flask port; change for prod (e.g., 8000)
backlog = 2048

# Worker processes - (2 * CPU cores) + 1 for optimal concurrency
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "sync"  # Default for CPU-bound Flask apps
worker_connections = 1000  # For threaded workers if needed
threads = 2  # Light threading per worker
timeout = 120  # Seconds before killing hung workers
keepalive = 2  # Reuse connections

# Process naming (helps with monitoring)
proc_name = "galaxy_preorder_app"

# Security & limits
limit_request_line = 4094  # Max header size
limit_request_fields = 100  # Max headers per request
max_requests = 1000  # Restart workers after N requests (anti-memory leak)
max_requests_jitter = 100  # Randomize restarts

# Logging (critical for prod debugging)
accesslog = "-"  # Log to stdout (use with Docker/supervisor)
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# PID file for process management
pidfile = "/tmp/gunicorn.pid"  # Adjust path for your env

# Preload app before forking workers (saves memory, good for large apps)
preload_app = True

# Daemon mode (use systemd/supervisor instead in prod)
daemon = False
