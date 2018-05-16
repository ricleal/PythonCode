#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging


if len(sys.argv) != 2:
    print("Use: {} <stream>".format(sys.argv[0]))
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
)

instance = sys.argv[1]

# The connected socket is duplicated to stdin/stdout
data = sys.stdin.readline().strip()
logging.info('My Service: Instance = {}. Request: = <{}>.'.format(
    instance, data))
sys.stdout.write("Server replied echo: {}\r\n".format(data))
