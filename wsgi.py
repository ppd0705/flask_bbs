#!/usr/bin/env python3

import app
from os.path import abspath
from os.path import dirname
import sys


sys.path.insert(0, abspath(dirname(__file__)))
application = app.configured_app()
