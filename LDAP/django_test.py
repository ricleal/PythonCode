#!/usr/bin/env python

from django_auth_ldap.backend import LDAPBackend


'''

SNS LDAP Authentication 

cd /home/rhf/git/reduction_service/src
python manage.py shell

'''
username = "rhf"

ldapobj = LDAPBackend()


user = ldapobj.populate_user(username)

# ERROR:
# [12/Jun/2015 14:15:19] WARNING [django_auth_ldap:396] Caught LDAPError while authenticating rhf: SERVER_DOWN({'info': '(unknown error code)', 'desc': "Can't contact LDAP server"},)

if user is None:
    print "1st try failed!"
    ldapobj.ldap.set_option(ldapobj.ldap.OPT_X_TLS_REQUIRE_CERT, ldapobj.ldap.OPT_X_TLS_NEVER)
    user = ldapobj.populate_user(username)

print user.is_anonymous()
