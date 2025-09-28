class Person:
        def __init__(self, name, age, major, grades):
            self.name = name
            self.age = age
            self.major = major
            self.grades = grades

        def __str__(self):
            return self.name + " is " +self.age

        def calc_avg_grade(self):
            return np.mean(self.grades)

brandon = Person("Brandon", 23, ["da"], [90, 93, 92])
print("brandon object grades: ", brandon.calc_avg_grade())