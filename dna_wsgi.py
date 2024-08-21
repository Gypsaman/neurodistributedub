import os
import time
import site
os.environ["TZ"] = "America/New_York"
time.tzset()

import sys
#
path = '/var/www/neurodistributedub'
if path not in sys.path:
    sys.path.append(path)
path = '/var/www/neurodistributedub/venv/lib/python3.9/site-packages'
if path not in sys.path:
    sys.path.append(path)

print(sys.path)
from webproject import create_app   # noqa
application = create_app()