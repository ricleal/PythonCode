import random
import pandas as pd

url ='https://www.national-lottery.co.uk/results/euromillions/draw-history/csv'
df = pd.read_csv(url, index_col=0,  sep=',')

lottoNumbers = range(1, 60)

tries = 0
while True:
    tries+=1
    luckyDip = random.sample(lottoNumbers, k=6) #Picks 6 numbers at random

    # subset of balls
    draws = df.iloc[:,0:7]

    # True where there is match
    matches = draws.isin(luckyDip)

    # Gives the sum of Trues
    sum_of_trues = matches.sum(1)

    # you are looking for matches where sum_of_trues is 6
    final = sum_of_trues[sum_of_trues == 6]
    if len(final) > 0:
        print("Took", tries)
        print(final)
        break