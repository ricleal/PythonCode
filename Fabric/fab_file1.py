# pylint: disable=C0103
from __future__ import print_function, with_statement

import os

from fabric.api import (cd, env, hosts, local, parallel, path, prefix, roles,
                        run, settings, sudo, task)
from fabric.contrib import files

from pprint import pprint
from functools import wraps

'''
This file is never called direcly
Use the command `fab`

If running this for the first time or without vietualenv:
pip3 install Fabric3  --user

# using file name and rules
fab -f fabfile.py -R dev deploy_dev
# or just the task and the default fabfile.py:
fab deploy_dev

Notes:
env.effective_roles : list of roles in @roles('staging','production')
'''


# Fabric hangs without this
env.shell = "/bin/bash -c"

# This is the definitions for ever
env.roledefs = {
    'staging': {
        'hosts': ['vagrant@127.0.0.1:2222'],
        'project_root': '/home/vagrant/sns-reduction',
    },
    'production': {
        'hosts': ['rhf@reduction.sns.gov'],
        'project_root': '/var/www/sns-reduction',
    }
}

def get_active_role_name():
    for role in env.roledefs.keys():
        if env.host_string in env.roledefs[role]['hosts']:
            return role

def append_to_active_role(role_name):
    env.roledefs[role_name].update({
        'src_root':
            os.path.join(env.roledefs[role_name]['project_root'], 'src')
    })

def set_active_role_as_env(role_name):
    for k, v in env.roledefs[role_name].items():
        if k in env and isinstance(env[k], list) and isinstance(v, list):
            env[k].extend(v)
        elif k in env and isinstance(env[k], list):
            env[k].append(v)
        else:
            env[k] = v

def apply_role(func):
    """
    This sets the env.roledefs[<active role>] as env variable
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        role_name = get_active_role_name()
        append_to_active_role(role_name)
        set_active_role_as_env(role_name)

        return func(*args, **kwargs)
    return wrapper

@task
@apply_role
@roles('staging', 'production')
def verbose():
    pprint(env['project_root'])
    pprint(env['src_root'])


