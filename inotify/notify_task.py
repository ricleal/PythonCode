# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
'''

Run as:
celery worker -A notify_task -l debug

Then
python3 notify_task

'''

import os
import pyinotify
import time
from os import stat

from celery import Celery

app = Celery('notify_task', broker='redis://localhost:6379/0')

SCAN_LOCATIONS = ["/home/rhf"]

class EventHandler(pyinotify.ProcessEvent):

    def bytes_to_english(self, no_of_bytes):
        #Helper function to convert number of bytes receives from os.stat into human radabale form
        # 1024 per 'level'
        suffixes = ['bytes', 'kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Yb']
        f_no = float(no_of_bytes)
        level = 0
        while(f_no > 1024.0):
            f_no = f_no / 1024.0
            level = level + 1
        if level == 0:
            return "%s %s" % (no_of_bytes, suffixes[level])
        return "%5.1f %s" % (f_no, suffixes[level])

    def get_stats(self, pathname, name):
        #Helper function to form the data dictionary for passing onto the database helper.
        stats = os.stat(pathname)
        return stats

    def process_IN_CREATE(self, event):
        #Called everytime a file / dir is created
        filestats = self.get_stats(event.pathname, event.name)
        print(filestats)
 
    def process_IN_DELETE(self, event):
        #Called everytime a file / dir is deleted
        print(event.pathname)

    def process_IN_MODIFY(self, event):
        #Called everytime a file / dir is modified
        filestats = self.get_stats(event.pathname, event.name)
        print(filestats)

@app.task
def monitor_folders():
    #Initialize the inotify watch manager
    wm = pyinotify.WatchManager()
    # watched events
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY 
    notifier = pyinotify.Notifier(wm, EventHandler())
    for location in SCAN_LOCATIONS:
        wdd = wm.add_watch(location, mask, rec=True)
    notifier.loop()

if __name__ == "__main__":
    monitor_folders.delay()
