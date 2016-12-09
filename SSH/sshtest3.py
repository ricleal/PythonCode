import os
import paramiko

from getpass import getpass

'''
Logs in the remote machine adds the client public key to the
authorised keys in the remote host

Set password = getpass() 
For the first login if authorised keys does not exist yet in the remote machine
'''

remote_host = "lealpc.ornl.gov"
#username = os.getlogin()
username = os.environ['USER']
password = None # getpass()
public_key_filename=os.path.expanduser('~/.ssh/id_rsa.pub')


def start(server, username, password=None,  key_filename=None):
	'''
	starts the client
	If password=None uses the key_filename
	'''
    try :
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if password:
            client.connect(server, port=22, username=username, password=password)
        else:
            client.connect(server, port=22, username=username, key_filename=key_filename) # no passwd needed
    except Exception as e:
        raise RuntimeError(e)
    return client

def deploy_key_if_it_doesnt_exist(client, key_filename):
    '''

    '''
    key = open(key_filename).read()
    client.exec_command('mkdir -p ~/.ssh/')

    command = '''
    KEY="%s"
    if [ -z "$(grep \"$KEY\" ~/.ssh/authorized_keys )" ];
    then 
        echo $KEY >> ~/.ssh/authorized_keys;
        echo key added.;
    fi;
    '''%key

    stdin, stdout, stderr  = client.exec_command(command)

    print(stdout.readlines())
    print(stderr.readlines())

    client.exec_command('chmod 644 ~/.ssh/authorized_keys')
    client.exec_command('chmod 700 ~/.ssh/')


client = start(remote_host, username, password,  key_filename=public_key_filename)

deploy_key_if_it_doesnt_exist(client, key_filename=public_key_filename)


while client:
    key = True
    cmd = input("Command to run: > ")
    if cmd == "":
        break
    chan = client.get_transport().open_session()
    print("** running '%s'" % cmd)
    chan.exec_command(cmd)
    while key:
        if chan.recv_ready():
            print("** recv:\n%s" % chan.recv(4096).decode('ascii'))
        if chan.recv_stderr_ready():
            print("** error:\n%s" % chan.recv_stderr(4096).decode('ascii'))
        if chan.exit_status_ready():
            print("** exit status: %s" % chan.recv_exit_status())
            key = False
            client.close()
client.close()

