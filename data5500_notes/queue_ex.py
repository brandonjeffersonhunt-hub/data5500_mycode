'''
This program executes a simple moving average trading strategy
but stores all the prices in memory as a list first
This program can be improved in memory efficiency by loading the prices
in one at a time, right when you need them, using a queue
'''
import os


# load all the prices from the file, into a Python List
# stock prices file
prices = []
line = file.readline()
print("line:", line)
fisrt_price = float(line)

# iterate through prices in list and run strategy
days= 5
buy = 0
profit = 0.0

while line:
    prices.append(float(line))

    if len(prices) == 6:
        current_price = prices[5]
        avg = (prices[0] + prices[1] + prices[2] + prices[3] + prices[4]) / 5
        if current_price > avg and buy ==0:
            print("buying at: ", p)
            buy = current_price
        elif p < avg and buy != 0: #sell
            print("selling at: ", p)
            tot_profit += current_price - buy
            print("trade profit: ", p - buy)
            buy = 0
        else:
            pass # do nothing today, except hopefully my position is becoming more profitable

        prices.pop(0)
    
    line = file.readline()
        
        
print("profit: ", profit)
print("percentage returns%: ", 100 * (profit/prices[0]))

input("press enter")
