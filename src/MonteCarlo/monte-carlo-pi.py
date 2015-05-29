'''
Created on Jun 20, 2012

@author: leal
'''

from random import random
from math import pow, sqrt

'''

http://niallohiggins.com/2007/07/05/monte-carlo-simulation-in-python-1/

Monte Carlo simulation in Python #1


I became interested in Monte Carlo simulation after reading Fooled By Randomness, 
the author of which makes numerous references to the power of these simulators. 
One of the first things I learned was that "Monte Carlo methods" is a term covering
 pretty much any use of pseudo-randomness to help solve any kind of problem. 
 Apparently, Monte Carlo is an old name for what is now commonly known as a roulette wheel,
  hence the relation to randomness.

One of the fascinating examples of a Monte Carlo simulator described in Fooled by Randomness 
is the use of pseudo-random numbers to calculate an approximation of the value of Pi. 
Imagine a dart board inside of a square. If you throw darts, in a random fashion, 
at the square, counting the number of darts which land on the dart board versus the
 number which land on the square, you can approximate Pi with some simple arithmetic.

After reading about this, I simply had to write a program to work it out. 
I figured Python would be a good language in which to hack it out. Indeed, 
it turns out that Python comes with a good pseudo-random number module in its 
standard library. Here is the code for my simple Pi approximator, which throws 
1,000,000 virtual darts:


Someone with no formal knowledge of geometry can compute the mysterious almost mystical Pi. 
How? By drawing a circle inside of a square and shooting random bullets into the picture 
(as in an arcade) specifying equal probabilities of hitting any point on the map 
(something called a uniform distribution). The ratio of bullets inside the circle divided by 
those j side and outside the circle will deliver a multiple of the mystical Pi, with 
possible infinite precision. Clearly this is not an efficient use of a computer as Pi 
can be computed analytically that is in a mathematical form, but the method can give some 
users more intuition about the subject matter than lines of equations. Some people's brains
and intuitions are oriented in such way that they are more capable of getting a point in
such a manner.

Pi is commonly defined as the ratio of a circle's circumference C to its diameter d:
pi = C/d



The area of a circle = PI * (radius * radius)
The area of a square = (length of one of its sides * lenght of one of its sides).

If the circle is inscribed inside a square that means the length of one of the sides of the
 square = 2 * radius of the circle. This means we can write the area of the square as 
 (2 * radius) * (2 * radius) = 4 * (radius * radius). So, if we divide the area of the 
 circle by the area of the square we get PI / 4. So, if we multiply the area of a circle 
 by 4 and divide the result by the area of the square that inscribes that circle we get 
 the value of PI.
The Monte Carlo method to calculate PI consists of generating random numbers and counting 
how many fall in the square and how many fall in the circle, then multiply by 4 the number
that fall in the circle and divide that by the number that fall in the square. To make it
easier to understand, here is PHP code that generates the value of PI using the Monte Carlo
method:

'''

def monte_carlo():
    DARTS=1000000
    hits = 0
    throws = 0


    for i in range (1, DARTS):
        throws += 1
        #  0 <= random number < 1
        # points generated inside the square
        x = random()
        y = random()
        # 0 <= dist < sqrt(2) = 1.4
        # we use the pythagoras' theorem to determine how many points are in inside the circle
        # It's hard to explain in words. Draw a square. Inscribe a circle inside the square.
        # Considering only the top right quadrant, you will see that any square trinagle you draw that has a
        # hypothenuse that starts from (0,0) and ends at the edge of the circle has a length equal to the
        # radius of the circle. Thus, using that idea and pythagoras' theorm we have that
        # for a circle inscribed in a square, hypothenuse^2 = radius ^2 = x-coordinate^2 + y-coordinate^2.
        dist = sqrt(x**2 + y**2)
        
        if dist <= 1.0:
            hits = hits + 1.0
    
    # all points are inside the square, so we just use DARTS for the number of points in the square
    # hits / throws = 1/4 Pi
    pi = 4 * (hits / throws)
    
    print "pi =%.2f, hits=%.2f, throws=%.2f, (hits / throws)=%.2f" %(pi,hits,throws,(hits / throws))



if __name__ == '__main__':
    
    monte_carlo()

