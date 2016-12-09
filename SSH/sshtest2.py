import os

import paramiko
import getpass

pw = getpass.getpass()

client = paramiko.SSHClient()
#client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def start():
    try :
        client.connect('127.0.0.1', port=22, username=os.environ['USER'], password=pw)
        return True
    except Exception as e:
        #client.close()
        print(e)
        return False

while start():
    key = True
    cmd = input("********** Command to run: ****************")
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

