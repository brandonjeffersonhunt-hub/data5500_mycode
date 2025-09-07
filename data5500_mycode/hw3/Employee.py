#2.  Create a class called Employee with attributes name and salary. 
# Implement a method within the class that increases the salary of the employee by a given percentage. 
# Instantiate an object of the Employee class with name = "John" and salary = 5000, increase the salary by 10%, and print the updated salary.

class Employee:             #Same as the last question, create the class and give it the attributes
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def increase_by_percentage(self, percent:float):        #add a means to increase the salary by an inputed percentage
        self.salary = self.salary * (1 + percent / 100)     #equation to divide the percent to a decimal and increase salary by that decimal
        return self.salary

emp = Employee(name = "John", salary = 5000)         #add john to the database

print(f"Name = {emp.name}, Salary = {emp.salary}") #Check to make sure John is added

updated_salary = emp.increase_by_percentage(10)     #increase the salary by 10 percent

print(f"Name = {emp.name}, Updated Salary = {updated_salary}")
