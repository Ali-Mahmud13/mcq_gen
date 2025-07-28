import logging
import os
from datetime import datetime

LOG_FILE= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), 'logs')

os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)



logging.basicConfig(level=logging.INFO, #confirmationt that things are working as expected
        filename=LOG_FILE_PATH,
        format='[%(asctime)s] %(lineno)d - %(levelname)s - %(message)s'
        )