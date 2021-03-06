import os
import logging

LOG_TO_DIR = '{{ FLASK_LOG_TO_DIR }}'
LOG_LEVEL = logging.getLevelName(os.environ.get("FLASK_LOG_LEVEL", "{{ FLASK_LOG }}"))

CALCULATE_WAIT_TIME = {{ FLASK_CALCULATE_WAIT_TIME }}
BID_CREATION_WAIT_TIME = {{ FLASK_BID_CREATION_WAIT_TIME }}
