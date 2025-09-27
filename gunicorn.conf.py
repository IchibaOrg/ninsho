#!/usr/bin/env python3
import os


bind = f"0.0.0.0:{os.getenv('APP_PORT', '8000')}"
reload = os.getenv('DEBUG', 'false').lower() == 'true'
worker_class = "uvicorn.workers.UvicornWorker"
workers = int(os.getenv('APP_NUM_WORKERS', '1'))
timeout = 15 * 60