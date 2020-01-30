#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/quaffle/")
sys.path.insert(0,"/var/www/quaffle/quaffle/")

import logging
logging.basicConfig(stream=sys.stderr)

from quaffle import app as application

