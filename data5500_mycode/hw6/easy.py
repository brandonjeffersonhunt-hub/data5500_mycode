def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

integers = [1,4,10,13,22,5]
result = calculate_sum(integers)
print(result)

#Chat prompt after writing the function:
'''
1. Given an array of integers, write a function to calculate the sum of all elements in the array.

Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.

Here is my assignment. I wrote the function, how do I analyze the time complexity...
'''
#The type of big O notation here is o(n) because it grows with the size of the array. It will do 0+1, then 0+1+4...