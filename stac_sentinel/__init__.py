import logging

from .sentinel import *

# quiet loggers
logging.getLogger('botocore').propagate = False
logging.getLogger('urllib3').propagate = False
logging.getLogger('requests').propagate = False
