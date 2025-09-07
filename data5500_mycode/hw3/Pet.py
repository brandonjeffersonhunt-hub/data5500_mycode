#Create a class called Pet with attributes name and age. 
# Implement a method within the class to calculate the age of the pet in equivalent human years. 
# Additionally, create a class variable called species to store the species of the pet. 
# Implement a method within the class that takes the species of the pet as input and returns the average lifespan for that species.

#Instantiate three objects of the Pet class with different names, ages, and species.
#Calculate and print the age of each pet in human years.
#Use the average lifespan function to retrieve and print the average lifespan for each pet's species.

class Pet:                      #create the class and its attributes
    def __init__(self, name: str, age: float, species: str):
        self.name = name
        self.age = age
        self.species = species
    
    def human_years_age(self):       #create the method to calculate the years
        if self.species.lower() == "dog":      #if the species is a dog (make lower so input caps doesnt matter)
            if self.age <= 2:
                return self.age*10.5        #chat said that the first two years of a dogs life = 21 human years
            else:
                return 21 + (self.age-2)*4  #after the first 2 years it is just 4 dog years for every human year
        if self.species.lower() == "cat":     #for cats, the first year =15, second = 24, and then 4 per human year
            if self.age == 1:
                return 15
            if self.age == 2:
                return 24
            else:
                return 24 + (self.age-2) *4
        else:                                   #for any other species we can just do the classic 7 years per human year
            return self.age * 7

    @classmethod            #chat recommended I use @classmethod because we are returning the average age of any pet in the species, not just a specific pet
    def average_lifespan(cls, species: str):        #create list of species avg lifespans
        lifespans = {
            "dog": 12,
            "cat": 15,
            "parrot": 50,
            "hamster": 3,
            "rabbit": 10
        }
        return lifespans.get(species.lower(), 10)   #Return the lifespan of the pet they entered, but put 10 if the one they input is not listed

#Test by creating 3 pets
pet1 = Pet(name = "Jerry", age = 5, species = "dog")
pet2 = Pet(name = "dora", age = 1, species = "Hamster")
pet3 = Pet(name = "Frank", age = 2, species = "Cat")

#print the name species and human years age
print(f"{pet1.name} the {pet1.species} is {pet1.human_years_age()} years old in human years")
print(f"{pet2.name} the {pet2.species} is {pet2.human_years_age()} years old in human years")
print(f"{pet3.name} the {pet3.species} is {pet3.human_years_age()} years old in human years")

#print the average age of the species
print(f"The average age of a {pet1.species} is {Pet.average_lifespan(pet1.species)} years")
print(f"The average age of a {pet2.species} is {Pet.average_lifespan(pet2.species)} years")
print(f"The average age of a {pet3.species} is {Pet.average_lifespan(pet3.species)} years")