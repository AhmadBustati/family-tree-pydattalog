from pyDatalog import pyDatalog 
import csv 

class Person(pyDatalog.Mixin):
    
    def __init__(self,name:str,gender:str,father=None,mother=None,spouse=None):

        super(Person,self).__init__()
        self.name = name 
        self.gender = gender
        self.father = father 
        self.mother = mother 
        self.spouse  = spouse


    def __repr__(self) -> str:
        return self.name 

    @pyDatalog.program()
    def Person():

        # 1.  Parents relationship asks if X is a parent of Y 
        Person.parent(X, Y) <=(Person.mother[Y] == X)  & (X != None) & (Y!=None)
        Person.parent(X,Y) <=(Person.father[Y] == X) & (X != None) & (Y!=None)

        # 2. Children relationship 
        # asks if X is a daughter of y
        Person.daughter(X,Y) <= (Person.gender[X]=="Female") & (Person.parent(Y,X)) 
        # asks if X is a son of y
        Person.son(X,Y) <= (Person.gender[X]=="Male") & (Person.parent(Y,X))

        # 3. Sibling rules 
        # If X and Y share the same parent they're siblings 
        Person.sibling(X,Y) <= (Person.mother[X]==Person.mother[Y]) & (Person.father[X]==Person.father[Y])&(X!=Y) & (Person.mother[X] != None) & (Person.father[X] !=None)
        # Brother rule :  X is brother of Y if they are siblings and X is a male 
        Person.brother(X,Y) <=  Person.sibling(X, Y) & (Person.gender[X] == "Male")
        # Sister rule : X is a sister of Y if they are siblings and X is a female
        Person.sister(X,Y) <= Person.sibling(X,Y) & (Person.gender[X]=="Female")

        # 4. Advanced relationships e.g. (uncles,aunts,cousins,niece, and nephew)
        # X is an uncle of Y if X is a brother to one of Y's parents 
        Person.uncle(X,Y) <= Person.parent(Z,Y) & Person.brother(X,Z)
        # X is an aunt of Y if X is a sister to one of Y's parents 
        Person.aunt(X,Y) <= Person.parent(Z,Y) & Person.sister(X,Z)
        # X is niece of Y if X is a female and Y is an uncle/aunt of X 
        Person.niece(X,Y) <= (Person.gender[X]=="Female") & (Person.uncle(Y,X))
        Person.niece(X,Y) <= (Person.gender[X]=="Female") & (Person.aunt(Y,X))
        # X is a nephew of Y if X is a male and Y is an uncle/aunt of X
        Person.nephew(X,Y) <= (Person.gender[X]=="Male") & (Person.uncle(Y,X))
        Person.nephew(X,Y) <= (Person.gender[X]=="Male") & (Person.aunt(Y,X))
        # X is a cousin  of Y if the parent of Y is either an uncle or an aunt of X 
        Person.cousin(X, Y) <= Person.parent(Z, Y) & Person.aunt(Z, X)
        Person.cousin(X,Y )<= Person.parent(Z, Y) & Person.uncle(Z, X)
        
        # 5. Handling in law relationships: 
        # X is the father in law of Y if X is the father of Y's spouse
        Person.father_in_law(X,Y) <= ((Person.father[Z]==X) & (Person.spouse[Y]==Z) &(X != None) & (Y !=None))
        # X is the mother in law of Y if X is the mother of Y's spouse 
        Person.mother_in_law(X,Y) <= ((Person.mother[Z]==X) & (Person.spouse[Y]==Z) &(X != None) & (Y !=None))
        

        # 6. Handling step relationships e.g. (step brother, step sister ):
        # X is a step mother of Y if X a spouse of X's father and not X's mother and X is a female 
        Person.step_mother(X,Y) <= ((Person.gender[X]=="Female") & (Person.spouse[X]==Person.father[Y])&(Person.mother[Y]!=X))
        # X is a step father of Y if X is a spouse of Y's mother and X is a male 
        Person.step_father(X,Y) <= ((Person.gender[X]=="Male") & (Person.spouse[X]==Person.mother[Y])&(Person.father[Y]!=X))
        # X is a step brother of Y if they don't share any parents and on of their parents are married and X is a male
        Person.step_brother(X, Y) <= (Person.parent(P, X)) & (Person.parent(Q, Y)) & (P != Q) & (Person.spouse[P] == Q) & (Person.gender[X]=="Male")
        # X is a step sister of Y if they don't share any parents and on of their parents are married and X is a female
        Person.step_sister(X, Y) <= (Person.parent(P, X)) & (Person.parent(Q, Y)) & (P != Q) & (Person.spouse[P] == Q) & (Person.gender[X]=="Female")

        # 7. Handling grandparents and great-grandparents:
        # X is a grandparent of Y if X is a parent of one of Y's parents 
        Person.grandparent(X,Y) <= (Person.parent(Y,Z))&(Person.parent(Z,Y))
        # X is a grandfather of Y if X is a grandparent of Y and X is a Male
        Person.grandfather(X,Y) <= (Person.grandparent(X,Y))&(Person.gender[X]=="Male")
        # X is a grandmother of Y if X is the mother of one of Y's parents
        Person.grandmother(X,Y) <= (Person.grandparent(X,Y))&(Person.gender[X]=="Female")
        # X is a great-grandparent of Y if X is a parent of one of Y grandparent 
        Person.great_grandparent(X,Y) <= (Person.parent(X,Z)) &(Person.grandparent(Z,Y))
        # X is a great-grandfather of Y if X is a male and a great grandparent of Y 
        Person.great_grandfather(X,Y) <= (Person.great_grandparent(X,Y)) & (Person.gender[X]=="Male")
        # X is a great-grandmother of Y if X  is a female and a great grandparent of Y 
        Person.great_grandmother(X,Y) <= (Person.great_grandparent(X,Y)) & (Person.gender[X]=="Female")

        # 8. Handling half sibling 
        # X is a half sibling of Y if they share one of the two parents 
        Person.half_sibling(X,Y) <= (Person.father[X]==Person.father[Y]) &(Person.mother[X]!=Person.mother[Y]) 
        Person.half_sibling(X,Y) <= (Person.father[X]!=Person.father[Y]) &(Person.mother[X]==Person.mother[Y])
        # X is a half brother of Y if X is a male and they are half siblings
        Person.half_brother(X,Y) <= (Person.gender[X]=="Male") & (Person.half_sibling(X,Y))
        # X is a half sister of Y if X is a male and they are half siblings
        Person.half_sister(X,Y) <= (Person.gender[X]=="Female") & (Person.half_sibling(X,Y))
        
        # 9. Handling siblings-in law and Niece/nephew in-law
        # X is the brother in law of Y if X is the brother of Y's spouse 
        Person.brother_in_law(X,Y) <= ((Person.brother(X,Z)) & (Person.spouse[Y]==Z) & (X != None) & (Y!= None))
        # X is the sister in law of Y if X is the sister of Y's spouse 
        Person.sister_in_law(X,Y) <= ((Person.sister(X,Z)) & (Person.spouse[Y]==Z) & (X != None) & (Y!= None))
        # X is a nephew in law to Y if X is a nephew of Y's spouse 
        Person.nephew_in_law(X,Y) <= (Person.nephew(X,Z))&(Person.spouse[Y]==Z)
        # X is a niece in law to Y if X is a nephew of Y's spouse 
        Person.niece_in_law(X,Y) <= (Person.niece(X,Z)) & (Person.spouse[Y]==Z)


    @staticmethod
    def from_csv_row(row):
        # Create a Person instance from a CSV row
        name, gender, father, mother, spouse = row
        return Person(name, gender, father, mother, spouse)
    



read_family_data = []
with open("family_tree.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Skip the header row
    for row in csvreader:
        person = Person.from_csv_row(row)
        read_family_data.append(person)

print(len(read_family_data))
print(read_family_data[0])

X = pyDatalog.Variable()
Y = pyDatalog.Variable()

# Check if Thanaa is a parent of Ahmad
# print(f"Parents of {Ahmad } {Person.parent(X, Ahmad)}")
# print(f"Daughters of {Thanaa} {Person.daughter(X,Thanaa)}")
# print(f"Siblings of {Ahmad} {Person.sibling(X,Y)}")
# print(f"Brothers of {Ahmad} {Person.brother(X,Ahmad)}")
# print(f"Sisters of {Ahmad} {Person.sister(X,Ahmad)}")
# print(f"{Person.uncle(Y,X)}\n------")
# print(Person.aunt(Y,X))
# print(Person.sibling(X,Y))
# print(Person.parent(X,Y))
# print(Person.niece(X,Y))
# print(Person.nephew(X,Y))
# print(Person.cousin(Bana,Y))
# print(Person.father_in_law(X,Y))
# print(Person.mother_in_law(X,Y))
# print(Person.brother_in_law(X,Y))
# print(Person.sister_in_law(X,Y))