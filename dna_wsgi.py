import os
import time
import site
os.environ["TZ"] = "America/New_York"
time.tzset()

import sys
#
path = '/var/www/dna'
if path not in sys.path:
    sys.path.append(path)
path = '/var/www/dna/venv/lib/python3.12/site-packages'
if path not in sys.path:
    sys.path.append(path)

print(sys.path)
from webproject import create_app   # noqa
application = create_app()