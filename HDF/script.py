#!/usr/bin/env python3
from log import Log

from datetime import datetime


l = Log()

now = datetime.now().time().strftime('%H:%M:%S')
print(now, "Done...")
