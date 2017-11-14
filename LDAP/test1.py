#!/usr/bin/env python
from __future__ import print_function

import ldap
import getpass
import sys

"""
Test connection on ORNL LDAP
Only works on the intranet

"""


url='ldaps://ldap-vip.sns.gov/'
username='uid=%s,ou=Users,dc=sns,dc=ornl,dc=gov'
#cert = '/etc/ssl/certs/ca-certificates.crt'

print("Username: ", end='')
user = sys.stdin.readline()
username = username%user
pwd = getpass.getpass()


try:
    print("Contacting LDAP....")
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

    ldapmodule_trace_level = 0
    ldapmodule_trace_file = sys.stderr

    l = ldap.initialize(url,
                        trace_level=ldapmodule_trace_level,
                        trace_file=ldapmodule_trace_file)

    l.simple_bind_s(username, pwd)
    l.unbind()
    print("*"*30, "\nIf I get here then it worked!")
except ldap.LDAPError, e:
    print(e)
