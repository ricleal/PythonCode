#!/usr/bin/python

'''
Created on Sep 12, 2013

@author: leal
'''



import collections

DECK_SIZE = 5

class Population(collections.deque):

    def __init__(self):
        super(Population, self).__init__(DECK_SIZE*[0], DECK_SIZE)

    def insertValue(self,value):
        self.appendleft(value)

class Entry(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value

def complexDeck():
    p = Population()

    e = Entry({"a":1})


    for i in range(0,10):
        e["a"]=i
        p.insertValue(e)
        print(p)


def simpleDecque():
    x = collections.deque(DECK_SIZE*[0], DECK_SIZE)
    print(x)
    x.appendleft(1)
    print(x)
    x.appendleft(2)
    print(x)
    x.appendleft(3)
    print(x)
    x.appendleft(4)
    print(x)
    x.appendleft(5)
    print(x)
    x.appendleft(6)
    print(x)
    x.appendleft(7)
    print(x)
    print("Last element stored on the deque:", x[0])



def main():
    simpleDecque()
    complexDeck()

if __name__ == "__main__":
    main()
