from subprocess import call
import tempfile

'''
Write and execute and temporary file.
Delete file after excecution
'''
with tempfile.NamedTemporaryFile() as temp:
    temp.write('echo $HOME > /tmp/test.ric')
    temp.flush()
    call(['/bin/sh',temp.name])
