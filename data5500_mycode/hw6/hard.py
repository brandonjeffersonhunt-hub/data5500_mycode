def max_diff(numbers):
    maximum = max(numbers)      #find the biggest number
    minimum = min(numbers)         #find the smallest #
    return maximum - minimum       #biggest difference = big num - small num

integers = [1,4,10,13,22,5]
result = max_diff(integers)
print(result)

#finding the max and min each use o(n) notation, so that is the time complexity.
