import multiprocessing

# Worker Processes
workers = 2
worker_class = 'sync'

# Logging
logfile = '/var/www/apps/ssp/app.log'
loglevel = 'info'
logconfig = None

socket_path = 'unix:/tmp/ssp.sock'
bind = socket_path
