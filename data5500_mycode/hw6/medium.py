def second_largest(numbers):
    return sorted(numbers, reverse = True)[1] #sort the list from largest to smallest and grab the second number in the list

integers = [1,4,10,13,22,5]
result = second_largest(integers)
print(result)

#I dont really have any idea what kind of notation sorted is so I asked chat

#this code uses o(n log n) for the sorted line but o(n) to grab from the index. So it is o(n log n)
#the sorted function divides the list into halves and compares until each part has 1 element. then it merges together