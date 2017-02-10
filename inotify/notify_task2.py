# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
'''

The Task is the SYNC not the monitor!!!!

Run as:
celery worker -A notify_task -l debug

See if in the celery log this show up:
[tasks]
    (.............)
  . notify_task.monitor_folders


Then
python3 notify_task

'''

import os
import pyinotify
import time
import logging

from os import stat
from celery import Celery

app = Celery('notify_task2', broker='redis://localhost:6379/0')

SCAN_LOCATIONS = ["/tmp"]

logger = logging.getLogger(__name__)


@app.task
def long_sync_files(file_path):
    logger.debug("Starting long_sync_files...: %s", file_path)
    for i in range(5):
        logger.debug("Syncing long_sync_files: %s", i)
        time.sleep(1)
    logger.debug("Ended long_sync_files...")

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        logger.info("CREATE: Path: %s | Event: %s", event.pathname, event.name)
        long_sync_files.delay(event.pathname)

    def process_IN_DELETE(self, event):
        logger.info("DELETE: Path: %s | Event: %s", event.pathname, event.name)

    def process_IN_MODIFY(self, event):
        logger.info("MODIFY: Path: %s | Event: %s", event.pathname, event.name)

@app.task
def monitor_folders():
    '''
    Celery function
    Motitor the SCAN_LOCATIONS
    '''
    wm = pyinotify.WatchManager()
    # watched events
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY 
    notifier = pyinotify.Notifier(wm, EventHandler())
    for location in SCAN_LOCATIONS:
        wdd = wm.add_watch(location, mask, rec=True)
    notifier.loop()


if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    logger.debug("Main starting...")
    monitor_folders.delay()
