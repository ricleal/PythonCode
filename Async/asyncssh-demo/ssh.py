import asyncio, asyncssh, sys

# Example
# ssh_config = {
#     "host": "login.newton.utk.edu",
#     "port": 22,
#     "username": "costrouc",
#     "client_keys": "/home/costrouc/.ssh/id_rsa_cluster",
#     "passphrase": "<not going to tell you>",
#     "password": <if using password client keys and passphrase not needed>"
# }

# I used this to hide my password from version control
from config import ssh_config

async def run_client():
    async with asyncssh.connect(**ssh_config) as conn:
        result = await conn.run('echo $TERM; stty size',
                                term_type='xterm-color',
                                term_size=(80, 24))
        print(result.stdout, end='')

        result = await conn.run('whoami')
        print(result.stdout, end='')

        result = await conn.run('pwd')
        print(result.stdout, end='')

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
