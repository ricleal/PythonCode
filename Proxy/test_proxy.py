#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
from pprint import pprint
import sys
import re


def get_urls_for_pac_files():
    """
    Return a list of possible auto proxy .pac files being used,
    based on the system registry (win32) or system preferences (OSX).
    @return: list of urls
    """
    pacFiles = []
    if sys.platform == 'win32':
        try:
            import _winreg as winreg  # used from python 2.0-2.6
        except:
            import winreg  # used from python 2.7 onwards
        net = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"
        )
        nSubs, nVals, lastMod = winreg.QueryInfoKey(net)
        subkeys = {}
        for i in range(nVals):
            thisName, thisVal, thisType = winreg.EnumValue(net, i)
            subkeys[thisName] = thisVal
        if 'AutoConfigURL' in subkeys.keys() and len(subkeys['AutoConfigURL']) > 0:
            pacFiles.append(subkeys['AutoConfigURL'])
    elif sys.platform == 'darwin':
        import plistlib
        sysPrefs = plistlib.readPlist(
            '/Library/Preferences/SystemConfiguration/preferences.plist')
        networks = sysPrefs['NetworkServices']
        # loop through each possible network (e.g. Ethernet, Airport...)
        for network in networks.items():
            netKey, network = network  # the first part is a long identifier
            if 'ProxyAutoConfigURLString' in network['Proxies'].keys():
                pacFiles.append(network['Proxies']['ProxyAutoConfigURLString'])
    return list(set(pacFiles))  # remove redundant ones


def get_proxy_urls_from_pac_files(pac_urls_list):
    '''
    Parsed the pac files and find all the possible
    proxies addresses
    '''
    proxy_url_list = []
    for thisPacURL in pac_urls_list:
        print 'Connecting to the PAC URL:\n  %s' % thisPacURL
        try:
            response = urllib2.urlopen(thisPacURL, timeout=2)
        except urllib2.URLError:
            print("Failed to find PAC URL '%s' " % thisPacURL)
            continue
        pacStr = response.read()
        possProxies = re.findall(
            r"PROXY\s([^\s;,:]+:[0-9]{1,5})[^0-9]", pacStr + '\n')
        for thisPoss in possProxies:
            proxUrl = 'http://' + thisPoss
            proxy_dic = {'http': proxUrl}
            proxy_url_list.append(proxy_dic)
    return proxy_url_list


def set_proxy(proxy_dic=None):
    '''
    proxy format: {'http': 'http://www.example.com:3128/'}
    To disable autodetected proxy pass an empty dictionary: {}
    '''
    if proxy_dic is None:
        # The default is to read the list of proxies from the environment variables <protocol>_proxy.
        # If no proxy environment variables are set, then in a Windows environment proxy settings are
        # obtained from the registry's Internet Settings section, and in a Mac OS X environment proxy
        # information is retrieved from the OS X System Configuration
        # Framework.
        proxy = urllib2.ProxyHandler()
    else:
        # If proxies is given, it must be a dictionary mapping protocol names to
        # URLs of proxies.
        proxy = urllib2.ProxyHandler(proxy_dic)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    print "Proxies returned by urllib2.getproxies:",
    pprint(urllib2.getproxies())


def check_update(url='http://www.sasview.org/latestversion.json', timeout=1):
    res = None
    req = urllib2.Request(url)
    try:
        print "* Direct connection..."
        res = urllib2.urlopen(req, timeout=timeout)
    except:
        try:
            print "** Proxy connection..."
            set_proxy()
            res = urllib2.urlopen(req, timeout=timeout)
        except:
            print "*** Pac Proxy connection..."
            pac_urls = get_urls_for_pac_files()
            proxy_urls = get_proxy_urls_from_pac_files(pac_urls)
            for proxy in proxy_urls:
                print "**** Trying proxy:", proxy
                try:
                    set_proxy(proxy)
                    res = urllib2.urlopen(req, timeout=timeout)
                    break  # suceeded!
                except Exception, e:
                    print "**** This proxy doesn't work...", proxy
                    pprint(e)
    if res is not None:
        print 50 * '-'
        print 'Got it!! ::', url
        print 50 * '-'
        content = json.loads(res.read().strip())
        pprint(content)
        print 50 * '-'

if __name__ == "__main__":
    check_update()
