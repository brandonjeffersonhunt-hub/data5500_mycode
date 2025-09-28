#3 Pillars of object oriented programming
#Encapsulation helps you protect your data from misuse. Makes your program more robus
#inheritance means an object can be derived from another object. Objects can have a parent/child relationship
#Polymorphism means child objects can change their behavior at run time. A child class will always have the functions its parent class has

#Polymorphism
class Car:
    def __init__(self, make, model, year, mileage, original_price):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.original_price = original_price
    
    def __str__(self):
        return str(self.year) + " " + self.make + " " + self.model
    
    def calc_value(self, current_year):
        age = current_year - self.year
        return self.original_price * (.94 ** age)

brandons_car = Car("Toyota", "Sequoia", 2001, 310000, 40000)
print(brandons_car)

glorias_car = Car("Toyota", "Camry", 2012, 140000, 20000)
print(glorias_car)

print(brandons_car.calc_value(2025))
print(glorias_car.calc_value(2025))


class AntiqueCar(Car):
    def calc_value(self, current_year):
        age = current_year - self.year
        return self.original_price * (1.03 ** age)    

calebs_car = AntiqueCar("Subaru", "Forester", 2011, 106000, 25000)

gregs_car = AntiqueCar("Cadillac", "Coup DeVille", 1978, 150000, 15000)

craigs_car = AntiqueCar("Ford", "Mustang", 1965, 10000, 15000)

zachs_car= Car("Toyota", "Camry", 2002, 200000, 20000)

alexs_car = AntiqueCar("Honda", "CRV", 2013, 131000, 22000)
car_lot = [brandons_car, calebs_car, gregs_car, craigs_car, zachs_car, alexs_car] #car objects

for car in car_lot:
    print(car, "value in 2025:", car.calc_value(2025))
