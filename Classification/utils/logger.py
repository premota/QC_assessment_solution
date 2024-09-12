"""
This script sets up logging for an application. 
It creates a unique log directory based on the current timestamp 
and configures logging to write both to a log file and to the console.
"""

import logging
import os
from datetime import datetime
import sys

logs_unique_dir = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", logs_unique_dir)
os.makedirs(logs_path, exist_ok = True)

log_file_path = os.path.join(logs_path, "Running_logs.log")




logging.basicConfig(
    format = "[%(asctime)s] %(lineno)d -%(levelname)s - %(message)s",
    level = logging.INFO,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)