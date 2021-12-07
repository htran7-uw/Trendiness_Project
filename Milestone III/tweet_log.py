import logging
import os.path
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_file = "tweet_result.log"
f = logging.FileHandler(log_file, mode='w')
f.setLevel(logging.INFO)

formatter = logging.Formatter(u"%(asctime)s: %(message)s")
f.setFormatter(formatter)

logger.addHandler(f)
