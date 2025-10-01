#Anytime you see n, that means the number (n) of inputs
#order adn big o are synonyms
#o(1) pops the first value
# o(n) needs to go through the list once (Avg, Max, Min) 
# o(log n) used for binary search. Half n over and over again to find the specific observation
#o(n^2) nested for loop

n=1000

for i in range(n):
    for j in range(n):
        print( i**j)

