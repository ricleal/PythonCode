from collections import UserList
from pprint import pprint

class MySequence(UserList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init")
        print(self.__len__())


l = MySequence()
l.append('a')
print(l)
pprint(dir(l))
