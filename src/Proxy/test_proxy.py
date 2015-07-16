#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
from pprint import pprint
import sys
import re

def _get_pac_files():
  """Return a list of possible auto proxy .pac files being used,
  based on the system registry (win32) or system preferences (OSX).
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

def get_proxy_from_pac_files():
  pacURLs = _get_pac_files()
  for thisPacURL in pacURLs:
    print 'get_proxy_from_pac_files is searching file:\n  %s' % thisPacURL
    try:
      response = urllib2.urlopen(thisPacURL, timeout=2)
    except urllib2.URLError:
      print("Failed to find PAC URL '%s' " % thisPacURL)
      continue
    pacStr = response.read()
    # find the candidate PROXY strings (valid URLS), numeric and non-numeric:
    possProxies = re.findall(
        r"PROXY\s([^\s;,:]+:[0-9]{1,5})[^0-9]", pacStr + '\n')
    for thisPoss in possProxies:
      proxUrl = 'http://' + thisPoss
      print 'get_proxy_from_pac_files: Trying prox URL:', proxUrl
      try:
        response = urllib2.urlopen(proxUrl, timeout=2)
        proxy_dic = {'http': proxUrl}
        return proxy_dic
      except urllib2.URLError:
        print("Failed to connect to prox URL '%s' " % proxUrl)
  return None

def get_proxy_windows():
  '''

  NOT USED!!


  [HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet
   Settings] "MigrateProxy"=dword:00000001
   "ProxyEnable"=dword:00000001
   "ProxyHttp1.1"=dword:00000000
   "ProxyServer"="http://ProxyServername:80"
   "ProxyOverride"="<local>"
  '''
  import _winreg
  proxy = _winreg.OpenKey(
      _winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings")
  server, type = _winreg.QueryValueEx(proxy, "ProxyServer")
  enabled, type = _winreg.QueryValueEx(proxy, "ProxyEnable")
  if enabled:
    return server
  return None


def set_roxy(proxy_dic=None):
  '''
  proxy format: {'http': 'http://www.example.com:3128/'}
  To disable autodetected proxy pass an empty dictionary: {}
  '''
  if proxy_dic is None:
    # The default is to read the list of proxies from the environment variables <protocol>_proxy.
    # If no proxy environment variables are set, then in a Windows environment proxy settings are
    # obtained from the registry's Internet Settings section, and in a Mac OS X environment proxy
    # information is retrieved from the OS X System Configuration Framework.
    proxy = urllib2.ProxyHandler()
  else:
    # If proxies is given, it must be a dictionary mapping protocol names to
    # URLs of proxies.
    proxy = urllib2.ProxyHandler(proxy_dic)
  opener = urllib2.build_opener(proxy)
  urllib2.install_opener(opener)
  print "Proxies:",
  pprint(urllib2.getproxies())


def check_update(url='http://www.sasview.org/latestversion.json', timeout=5):
  try:
    req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req,  timeout=timeout)
    except:
        proxy_from_pac = get_proxy_from_pac_files()
        set_roxy(proxy_from_pac)
        res = urllib2.urlopen(req,  timeout=timeout)
    content = json.loads(res.read().strip())
    pprint(content)
  except Exception, e:
    print "Failed!"
    pprint(e)


if __name__ == "__main__":
  # set_roxy({}) # No proxy!
  set_roxy()  # default
  check_update()
  # pac_files = get_pac_files()
  # print 'pac_files', pac_files
  # proxies_from_pac = proxy_from_pac_files(pac_files)
  # print 'proxies_from_pac:', proxies_from_pac
