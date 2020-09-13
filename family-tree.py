from os.path import join, dirname, isfile
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

class Person(object):
    def __init__(self, id = "", name = "", lastName = "", dateOfBirth = "", alive = "", gender = "",
     parent1 = "", parent2 = "", supose = "" ):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.alive = alive
        self.gender = gender
        self.parent1 = parent1
        self.parent2 = parent2
        self.supose = supose


this_folder = dirname(__file__)
do = True
fileName = ""

def getFamilyTreeModel(debug = False):
    """
    A function that gets meta-model from language description and export it to dot
    and instantiate model and export it to dot       
    """
    family_tree_meta = metamodel_from_file(join(this_folder, 'family-tree.tx'), debug=debug)
    metamodel_export(family_tree_meta, join(this_folder, 'family-tree_meta.dot'))
    family_tree_model = family_tree_meta.model_from_file(join(this_folder, fileName))
    model_export(family_tree_model, join(this_folder, 'family-tree.dot'))
    return family_tree_model

def checkFirstNameNotNull(person):
    """
    Returns persons first name if not null.
    """
    if person.firstName is not None:
        return person.firstName
    return ""

def checkLastNameNotNull(person):
    """
    Returns persons last name if not null.
    """
    if person.lastName is not None:
        return person.lastName
    return ""

def bornOn(person):
    """
    A function that prints a person's date of birth.
    """
    if person.dateOfBirth:
        print("Date of birth: {}.{}.{}.".format(person.dateOfBirth.day, person.dateOfBirth.month, person.dateOfBirth.year))
    else:
        print("Date of birth: unknown.")

def showSpouses(person):
    """
    A function that prints a person's spouse or spouses.
    """
    if person.spouses:
        print("Spouses:")
        for sp in person.spouses:
            if sp.since:
                print("\t{} {}, since {}.{}.{}.".format(checkFirstNameNotNull(sp.person), checkLastNameNotNull(sp.person), sp.since.day, sp.since.month, sp.since.year))
            else:
                print("\t{} {}".format(checkFirstNameNotNull(sp.person), checkLastNameNotNull(sp.person)))

def showParents(person):
    """
    A function that prints a person's parents.
    """
    if person.parent1 and person.parent2:
        print("Parents: {} {} and {} {}".format(checkFirstNameNotNull(person.parent1), checkLastNameNotNull(person.parent1),
        checkFirstNameNotNull(person.parent2), checkLastNameNotNull(person.parent2)))
    else:
        if person.parent1:
            print("Parent: {} {}".format(checkFirstNameNotNull(person.parent1), checkLastNameNotNull(person.parent1)))
        if person.parent2:
            print("Parent: {} {}".format(checkFirstNameNotNull(person.parent2), checkLastNameNotNull(person.parent2)))
        if person.parent1 is None and person.parent2 is None:
            print("No data about parents.")    

def showBrothersAndSisters(person):
    """
    A function that prints a person's brothers and sisters.
    """
    brothersAndSisters = []
    if person.parent1:
        for c in person.parent1.children:
            if not c.person.name == person.name:
                brothersAndSisters.append(Person(c.person.name, c.person.firstName, c.person.lastName))
    exists = False
    if person.parent2:   
        for c in person.parent2.children:
            if not c.person.name == person.name:
                for bns in brothersAndSisters:
                    if bns.id == c.person.name:
                        exists = True
                if not exists:
                    brothersAndSisters.append(Person(c.person.name, c.person.firstName, c.person.lastName))
    if brothersAndSisters:
        print("Brothers and sisters:")
        for bns in brothersAndSisters:
            print("\t{} {}".format(bns.name, bns.lastName))
    else:
        print("No brothers and sisters.")

def showChildren(person):
    """
    A function that prints a person's children.
    """
    if person.children:
        print("Children:")
        for c in person.children:
            print("\t{} {}".format(checkFirstNameNotNull(c.person), checkLastNameNotNull(c.person)))
    else:
        print("\tNo children.")

def showGrandparents(person):
    """
    A function that prints out grandparents of a person.
    """
    if person.parent1 is not None and person.parent2 is not None:
        if person.parent1.parent1 is not None and person.parent1.parent2 is not None and person.parent2.parent1 is not None and person.parent2.parent2 is not None:
            print("Grandparents from {}'s side are {} {} and {} {}, from {}'s side are {} {} and {} {}".format(person.parent1.firstName, person.parent1.parent1.firstName, person.parent1.parent1.lastName, person.parent1.parent2.firstName, person.parent1.parent2.lastName,     person.parent2.firstName, person.parent2.parent1.firstName, person.parent2.parent1.lastName, person.parent2.parent2.firstName, person.parent2.parent2.lastName))
        else:
            if person.parent1.parent1 is not None and person.parent1.parent2 is not None:
                print("Grandparents from {}'s side are {} {} and {} {}".format(person.parent1.firstName, person.parent1.parent1.firstName, person.parent1.parent1.lastName, person.parent1.parent2.firstName, person.parent1.parent2.lastName))
            if person.parent2.parent1 is not None and person.parent2.parent2 is not None:
                print("Grandparents from {}'s side are {} {} and {} {}".format(person.parent2.firstName, person.parent2.parent1.firstName, person.parent2.parent1.lastName, person.parent2.parent2.firstName, person.parent2.parent2.lastName))
            if person.parent1.parent1 is not None:
                print("Grandparent from {}'s side is {} {}".format(person.parent1.firstName, person.parent1.parent1.firstName, person.parent1.parent1.lastName))
            if person.parent1.parent2 is not None:
                print("Grandparent from {}'s side is {} {}".format(person.parent1.firstName, person.parent1.parent2.firstName, person.parent1.parent2.lastName))
            if person.parent2.parent1 is not None:
                print("Grandparent from {}'s side is {} {}".format(person.parent2.firstName, person.parent2.parent1.firstName, person.parent2.parent1.lastName))
            if person.parent2.parent2 is not None:
                print("Grandparent from {}'s side is {} {}".format(person.parent1.firstName, person.parent2.parent2.firstName, person.parent2.parent2.lastName))
            if person.parent1.parent1 is None and person.parent1.parent2 is None and person.parent2.person1 is None and person.parent2.parent2 is None:
                print("No data about grandparents")
    else:
        print("No data about parents, also about grandparents")

def showAunts(person):
    """
    A function that prints aunts of a person.
    """
    Aunts=[]
    Sisters=[]
    if person.parent1:
        Aunts=findSisters(person.parent1)
    if person.parent2:
        Sisters=findSisters(person.parent2)
        for s in Sisters:
            Aunts.append(s)
    if Aunts:                        
        print("Aunts are:")  
        for aunt in Aunts:
            print("\t{} {}".format(aunt.name, aunt.lastName))

def showUncles(person):
    """
    A function that prints uncles of a person.
    """
    Uncles=[]
    if person.parent1 is not None and person.parent1.gender=='female':
        Uncles=findBrothers(person.parent1)
    if person.parent2 is not None and person.parent2.gender=='female':
        Uncles=findBrothers(person.parent2)        
    if Uncles:                        
        print("Uncles are:")  
        for uncle in Uncles:
            print("\t{} {}".format(uncle.name, uncle.lastName))


def findSisters(person):
    """
    A function that finds sisters of a person.
    Returns: a list of sisters(Person).
    """
    Sisters=[]
    if person.parent1 is not None:
        if person.parent1.children:
            for child in person.parent1.children:
                if not child.person.name == person.name:
                    if child.person.gender == 'female':
                        Sisters.append(Person(child.person.name, child.person.firstName, child.person.lastName))
            exist=False
    if person.parent2 is not None:
        if person.parent2.children:
            for child in person.parent2.children:
                exist=False
                if not child.person.name == person.name:
                    if child.person.gender == 'female':
                        for sis in Sisters:
                            if sis.id == child.person.name:   
                                exist=True 
                        if not exist:
                            Sisters.append(Person(child.person.name, child.person.firstName, child.person.lastName))
    return Sisters

def showSisters(person):
    """
    A function that prints a person's sisters.
    """
    Sisters=[]
    Sisters=findSisters(person)
    if Sisters:                        
        print("Sisters are:")  
        for s in Sisters:
            print("\t{} {}".format(s.name, s.lastName))

def findBrothers(person):
    """
    A function that finds a person's brothers.
    Return: list of brothers(Person).
    """
    Brothers=[]
    if person.parent1 is not None:
        if person.parent1.children:
            for child in person.parent1.children:
                if not child.person.name == person.name:
                    if child.person.gender == 'male':
                        Brothers.append(Person(child.person.name, child.person.firstName, child.person.lastName))
            exist=False
    if person.parent2 is not None:
        if person.parent2.children:
            for child in person.parent2.children:
                exist=False
                if not child.person.name == person.name:
                    if child.person.gender == 'male':
                        for bro in Brothers:
                            if bro.id == child.person.name:   
                                exist=True 
                        if not exist:
                            Brothers.append(Person(child.person.name, child.person.firstName, child.person.lastName))
    return Brothers

def showBrothers(person):
    """
    A function that prints a person's brothers.
    """
    Brothers=[]
    Brothers=findBrothers(person)
    if Brothers:                        
        print("Brothers are:")  
        for b in Brothers:
            print("\t{} {}".format(b.name, b.lastName))

#def showSistersInLaw(person):

#    SistersInLaw=[]
#    Brothers=[]
#    Brothers=findBrothers(person)
#    for brother in Brothers:
#        print("ISPISI {}".format(brother.supose))
#    if SistersInLaw:                        
#        print("Sisters in law are:")  
#        for sl in SistersInLaw:
 #           print("\t{} {}".format(sl.name, sl.lastName))

def displayPersonData(personId,  debug = False):
    family_tree_model = getFamilyTreeModel()
    found = False
    for person in family_tree_model.persons:
        if person.name == personId:
            print("\n{} {}".format(checkFirstNameNotNull(person), checkLastNameNotNull(person)))
            bornOn(person)
            showSpouses(person)
            showParents(person)
            showBrothersAndSisters(person)
            showChildren(person)
            found = True
    if not found:
        print("The peson {} doesn't exist!".format(personId))

def chooseRelationship():
    print("Choose relationship:")
    print("1 - parents")
    print("2 - brothers and sisters")
    print("3 - grandparents")
    print("4 - aunts")
    print("5 - uncles")
    print("6 - sisters in law")
    print("7 - brother in law")
    choise = input()
    print("Enter person")
    personId = input()
    family_tree_model = getFamilyTreeModel()
    found = False
    for person in family_tree_model.persons:
        if person.name == personId:
            found = True
            if choise == "1":
                showParents(person)
            if choise == "2":
                showBrothersAndSisters(person)
            if choise == "3":
                showGrandparents(person)
            if choise == "4":
                showAunts(person)
            if choise == "5":
                showUncles(person)
            if choise == "6":
                showParents(person)
                #showSistersInLaw(person)
            if choise == "7":
                showParents(person)
    if not found:
        print("The peson {} doesn't exist in this family!".format(personId))

if __name__ == '__main__':
    while do:
        print("Please enter filename")
        fileName = input()
        if isfile(join(this_folder, fileName)):
            #proveriti da model li odgovara gramatici
            do = False
        else:
            print("\n\t\tWrong filename\n")
    do = True
    while do:
        print("\nChoose one of the options: ")
        print("1 - show person data")
        print("2 - show persons relationships")
        print("3 - show relationship")
        print("4 - display results from query file")
        print("5 - end")
        choise = input()
        if choise == "1":
            displayData = True
            while displayData:
                print("\nEnter person name, (enter back to go back)") 
                personId = input()
                if personId.lower() != "back":
                    displayPersonData(personId)
                else:
                    displayData = False
        else:
            if choise == "2":
                chooseRelationship()
            else:
                if choise == "3":
                    continue
                else:
                    if choise == "4":
                        pass
                    else:
                        if choise == "5":
                            do = False
                        else:
                            print("wrong entry")

