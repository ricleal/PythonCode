import os
import sys
import paramiko

from getpass import getpass

'''
Logs in the remote machine adds the client public key to the
authorised keys in the remote host

Set password = getpass() 
For the first login if authorised keys does not exist yet in the remote machine

Accepts live log:
(in bash for example:)
for i in {1..10}; do echo $i; sleep 1s; done

'''

server_hostname = "analysis.sns.gov"
server_port = 22
#username = os.getlogin()
username = os.environ['USER']
public_key_filename=os.path.expanduser('~/.ssh/id_rsa.pub')


#
#
#

def deploy_key_if_it_doesnt_exist(client, public_key_filename):
    '''

    '''
    key = open(public_key_filename).read()
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

#
#
#

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting with public key.")
    client.connect(server_hostname, port=server_port, username=username, key_filename=public_key_filename)
except (paramiko.AuthenticationException, paramiko.BadHostKeyException) as e:
    try:
        print("Connecting with password.")
        password = getpass()
        client.connect(server_hostname, port=server_port, username=username, password=password)
        deploy_key_if_it_doesnt_exist(client, public_key_filename)
    except paramiko.AuthenticationException as e:
        print("Authenctication error! Wrong password :)")
        sys.exit(-1)

while True:
    key = True
    cmd = input("Command to run: > ")
    if cmd == "":
        break
    chan = client.get_transport().open_session()
    print("** running '%s'" % cmd)
    chan.exec_command(cmd)
    while key:
        if chan.recv_ready():
            print("** stdout:\n%s" % chan.recv(4096).decode('utf-8'))
        if chan.recv_stderr_ready():
            print("** stderr:\n%s" % chan.recv_stderr(4096).decode('utf-8'))
        if chan.exit_status_ready():
            print("** exit status: %s" % chan.recv_exit_status())
            key = False
            #client.close()
client.close()

