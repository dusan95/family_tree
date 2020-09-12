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

def bornOn(person):
    """
    A function that prints out persons date of birth.
    """
    if person.dateOfBirth is not None :
        print("\n{} {} date of birth {}.{}.{}.".format(person.firstName, person.lastName, person.dateOfBirth.day, person.dateOfBirth.month, person.dateOfBirth.year))
    else:
        print("{} {} unknown date of birth.".format(person.firstName, person.lastName))

def showSpouses(person):
    """
    A function that prints out persons spouse or spouses.
    """
    if person.spouses is not None :
        for sp in person.spouses:
            if sp.since is not None:
                print("Spouse {} {}, since {}.{}.{}.".format(sp.person.firstName, sp.person.lastName, sp.since.day, sp.since.month, sp.since.year))
            else:
                print("Spouse {} {}".format(sp.person.firstName, sp.person.lastName))

def showParents(person):
    """
    A function that prints out persons parents.
    """
    if person.parent1 is not None and person.parent2 is not None:
        print("Parents: {} {} and {} {}".format(person.parent1.firstName, person.parent1.lastName, person.parent2.firstName, person.parent2.lastName))
    else:
        if person.parent1 is not None:
            print("Parent: {} {}".format(person.parent1.firstName, person.parent1.lastName))
        if person.parent2 is not None:
            print("Parent: {} {}".format(person.parent2.firstName, person.parent2.lastName))

def showBrothersAndSisters(person):
    """
    A function that prints out brothers and sisters of a person.
    """
    brothersAndSisters = []
    if person.parent1 is not None:
        for c in person.parent1.children:
            if not c.person.name == person.name:
                brothersAndSisters.append(Person(c.person.name, c.person.firstName, c.person.lastName))
        exists = False
    if person.parent2 is not None:   
        for c in person.parent2.children:
            if not c.person.name == person.name:
                for bns in brothersAndSisters:
                    if bns.id == c.person.name:
                        exists = True
                if not exists:
                    brothersAndSisters.append(Person(c.person.name, c.person.firstName, c.person.lastName))
    if brothersAndSisters.count != 0:
        print("Brothers and sisters:")
        for bns in brothersAndSisters:
            print("\t{} {}".format(bns.name, bns.lastName))

def displayPersonData(personId,  debug = False):
    family_tree_model = getFamilyTreeModel()
    found = False
    for person in family_tree_model.persons:
        if person.name == personId:
            bornOn(person)
            showSpouses(person)
            showParents(person)
            showBrothersAndSisters(person)
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
    if choise == "1":
        showParents(personId)
    if choise == "2":
        showBrothersAndSisters(personId)
    if choise == "3":
        showParents(personId)
    if choise == "4":
        showParents(personId)
    if choise == "5":
        showParents(personId)
    if choise == "6":
        showParents(personId)
    if choise == "7":
        showParents(personId)

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
        print("2 - show perons relationships")
        print("3 - show relationship")
        print("4 - end")
        choise = input()
        if(choise == "1"):
            print("Enter person name") 
            personId = input()
            displayPersonData(personId)
        if(choise == "2"):
            chooseRelationship()
        if choise == "3":
            continue
        if(choise == "4"):
            do = False
        else:
            print("wrong entry")

