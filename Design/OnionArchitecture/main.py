from disk import Disk
from operations.magic import some_magic


d = Disk("/dev/sda1")
d.read()

value = some_magic(2,3)

d.write(value)

