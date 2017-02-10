# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import pyinotify

from celery_config import app

SCAN_LOCATIONS = ["/tmp", "/var"]

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
        filestats = {'path':pathname, 'name':name}
        filestats['ATime'] = time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(stats[stat.ST_ATIME]))
        filestats['CTime'] = time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(stats[stat.ST_CTIME]))
        filestats['MTime'] = time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(stats[stat.ST_MTIME]))
        filestats['size'] = stats[stat.ST_SIZE]
        filestats['size_human'] = self.bytes_to_english(stats[stat.ST_SIZE])
        if stat.S_ISDIR(stats[stat.ST_MODE]):
            filestats['type'] = 'Directory'
        elif stat.S_ISLNK(stats[stat.ST_MODE]):
            filestats['type'] = 'Symbolic link'
        else:
            filestats['type'] = 'File'
        return filestats

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

