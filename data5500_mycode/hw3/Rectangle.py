#1.    Create a class called Rectangle with attributes length and width. 
# Implement a method within the class to calculate the area of the rectangle. 
# Instantiate an object of the Rectangle class with length = 5 and width = 3, and print its area.

class Rectangle:        #define the class rectangle
    def __init__(self, length: float, width: float): #this function will automatically run anytime i create a new rectangle object 
                                                     #and it will assign the values of length and width 
        self.length = length #this stores the rectangles length
        self.width = width #this stores the rectangles width

#define a method to calculate the area (l*w)
    def area(self):
        return self.length * self.width

#Create a rectagle with width of 3 and length of 5
rect = Rectangle(length = 5, width = 3)

print(f"Rectangle with width of 3 and length of 5 has an area of {rect.area()}") #Show the area
