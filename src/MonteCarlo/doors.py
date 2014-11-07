'''
Created on Nov 6, 2014

@author: rhf

Monte Carlo simulation for the Monty Hall problem:

Suppose you're on a game show, and you're given the choice of three doors:
Behind one door is a car; behind the others, goats. 
You pick a door, say No. 1, and the host, who knows what's behind the doors,
opens another door, say No. 3, which has a goat. He then says to you,
"Do you want to pick door No. 2?" Is it to your advantage to switch your choice?

 Under the standard assumptions, contestants who switch have a 2/3 chance of winning the car, 
 while contestants who stick to their choice have only a 1/3 chance.

'''
import random

# doors:
# index : prize 
# 1 means prize
doors = {1:0, 2:1, 3:0}
nTries = 10000

class Result:
    Win = True
    Loose = False

def shuffleDoors():
    global doors
    keys =  list(doors.keys())
    random.shuffle(keys)
    doors = dict([(key, doors[key]) for key in keys])
    
def pickADoorNumber():
    return random.choice(doors.keys())

def doorHasAPrize(doorNumber):
    if doors[doorNumber] == 1:
        return True
    else:
        return False

def keepDoor(doorNumber):
    if doorHasAPrize(doorNumber):
        return Result.Win
    else:
        return Result.Loose

def swapDoor(doorNumber):
    if doorHasAPrize(doorNumber):
        return Result.Loose
    else:
        return Result.Win

        

def main():
    swapWins = 0
    keepWins = 0
    for i in range(nTries):
        shuffleDoors()
        doorNumber = pickADoorNumber()
        
        if keepDoor(doorNumber) == Result.Win:
            keepWins+=1
        
        if swapDoor(doorNumber) == Result.Win:
            swapWins+=1
    
    print "Swap wins", swapWins, " : Keep Wins", keepWins
    print "Swap wins %.2f %% : Keep Wins %.2f %%" % (float(swapWins)/nTries*100.0,float(keepWins)/nTries*100.0)
    
if __name__ == '__main__':
    main()