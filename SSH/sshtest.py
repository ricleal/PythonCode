import paramiko
import getpass

pw = getpass.getpass()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.connect('127.0.0.1', password=pw)

while True:
    cmd = input("Command to run: ")
    if cmd == "":
        break
    chan = client.get_transport().open_session()
    print( "running '%s'" % cmd)
    chan.exec_command(cmd)
    print( "exit status: %s" % chan.recv_exit_status())

client.close()

