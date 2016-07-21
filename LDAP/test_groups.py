#!/usr/bin/env python
import ldap
import getpass
import sys
from pprint import pprint

"""
Only works on the intranet

Get's all IPTS numbers and users assigned
"""


url='ldaps://data.sns.gov/'
all_groups = "ou=Groups,dc=sns,dc=ornl,dc=gov"

# print "Username?"
# user = sys.stdin.readline()
# username = username%user
# pwd = getpass.getpass()


try:
    print "Contacting LDAP...."
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

    ldapmodule_trace_level = 0 //2
    ldapmodule_trace_file = sys.stderr

    l = ldap.initialize(url,
                        trace_level=ldapmodule_trace_level,
                        trace_file=ldapmodule_trace_file)


    results = l.search(all_groups, ldap.SCOPE_SUBTREE, "(&(cn=IPTS*)(description=proposal)(memberUid=*))", ["cn","memberUid"])

    while 1:
        result_type, result_data = l.result(results, 0)
        if (result_data == []):
            break
        else:
            if result_type == ldap.RES_SEARCH_ENTRY and result_data is not None:
                print "*"*80
                pprint(result_data[0][1]['cn'])
                pprint(result_data[0][1]['memberUid'])


    l.unbind()
    print "*"*30, "\nIf I get here then it worked!\n","*"*30
except ldap.LDAPError, e:
    print e
