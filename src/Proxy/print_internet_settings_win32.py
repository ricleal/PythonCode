#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def print_internet_settings():
    """
    """
    if sys.platform == 'win32':
        try:
            import _winreg as winreg  # used from python 2.0-2.6
        except:
            import winreg  # used from python 2.7 onwards
        net = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"
        )
        n_subs, n_vals, last_mod = winreg.QueryInfoKey(net)
        for i in range(n_vals):
            this_name, this_val, thisType = winreg.EnumValue(net, i)
            print this_name, '::', this_val, '::', thisType
         
    else:
        print "Not win32! ->",  sys.platform

if __name__ == "__main__":
    print_internet_settings()