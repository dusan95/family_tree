from os.path import join, dirname, isfile
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx import metamodel_for_language

class Person(object):
    def __init__(self, id = "", name = "", lastName = ""):
        self.id = id
        self.name = name
        self.lastName = lastName

this_folder = dirname(__file__)
do = True
fileName = ""

def getFamilyTreeModel(debug = False):
    """
    A function that gets meta-model from language description, instantiate model
    and export them to dot   
    """
    family_tree_meta = metamodel_from_file(join(this_folder[:len(this_folder)-5], 'family_tree_dsl/family-tree.tx'), debug=debug)
    metamodel_export(family_tree_meta, join(this_folder, 'family-tree_meta.dot'))
    family_tree_model = family_tree_meta.model_from_file(join(this_folder, fileName))
    model_export(family_tree_model, join(this_folder, 'family-tree.dot'))
    return family_tree_model

def checkIfPersonExistsInModel(personId):
    family_tree_model = getFamilyTreeModel()
    found = False
    for person in family_tree_model.persons:
        if person.name == personId:
            found = True
    return found

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
                print("\t{} {}, since {}.{}.{}.".format(sp.person.firstName, sp.person.lastName, sp.since.day, sp.since.month, sp.since.year))
            else:
                print("\t{} {}".format(sp.person.firstName, sp.person.lastName))

def showParents(person):
    """
    A function that prints a person's parents.
    """
    if person.parent1 and person.parent2:
        print("Parents: {} {} and {} {}".format(person.parent1.firstName, person.parent1.lastName,
        person.parent2.firstName, person.parent2.lastName))
    else:
        if person.parent1:
            print("Parent: {} {}".format(person.parent1.firstName, person.parent1.lastName))
        if person.parent2:
            print("Parent: {} {}".format(person.parent2.firstName, person.parent2.lastName))
        if person.parent1 is None and person.parent2 is None:
            print("No data about parents.")    

def findBrothersAndSisters(person):
    brothersAndSisters = []
    if person.parent1:
        for c in person.parent1.children:
            if not c.person.name == person.name:
                brothersAndSisters.append(Person(c.person.name, c.person.firstName, c.person.lastName))
    if person.parent2:   
        for c in person.parent2.children:
            if not c.person.name == person.name:
                exists = False
                for bns in brothersAndSisters:
                    if bns.id == c.person.name:
                        exists = True
                if not exists:
                    brothersAndSisters.append(Person(c.person.name, c.person.firstName, c.person.lastName))
    return brothersAndSisters

def showBrothersAndSisters(person):
    """
    A function that prints a person's brothers and sisters.
    """
    brothersAndSisters = findBrothersAndSisters(person)
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
            print("\t{} {}".format(c.person.firstName, c.person.lastName))
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

def showSistersInLaw(person):
    """
    A function that prints a person's sisters in law.
    """
    SistersInLaw=[]
    Brothers=[]
    Brothers=findBrothers(person)
    for brother in Brothers:
        person=getPerson(brother.id)
        for s in person.spouses:
            SistersInLaw.append(Person(s.person.name, s.person.firstName, s.person.lastName))
    if SistersInLaw:                        
        print("Sisters in law are:")  
        for sl in SistersInLaw:
            print("\t{} {}".format(sl.name, sl.lastName))

def showBrothersInLaw(person):
    """
    A function that prints a person's brothers in law.
    """
    BrothersInLaw=[]
    Sisters=[]
    Sisters=findSisters(person)
    for sister in Sisters:
        person=getPerson(sister.id)
        for s in person.spouses:
            BrothersInLaw.append(Person(s.person.name, s.person.firstName, s.person.lastName))
    if BrothersInLaw:                        
        print("Brothers in law are:")  
        for bro in BrothersInLaw:
            print("\t{} {}".format(bro.name, bro.lastName))

def showGrandchildren(person):
    """
    A function that prints a person's grandchildren.
    """
    Grandchildren=[]
    if person.children:
        for ch in person.children:
            if ch.person.children:
                for c in ch.person.children:
                    Grandchildren.append(Person(c.person.name, c.person.firstName, c.person.lastName))

    if Grandchildren:
        print("Grandchildren:")
        for c in Grandchildren:
            print("\t{} {}".format(c.name, c.lastName))
    else:
        print("\tNo grandchildren.")

def showNephews(person):
    """
    A function that prints a person's nephews.
    """
    Sisters=[]
    Brothers=[]
    Nephews=[]
    Sisters=findSisters(person)
    Brothers=findBrothers(person)
    if Sisters or Brothers:
        if Sisters:
            for sister in Sisters:
                person=getPerson(sister.id)
                if person.children:
                    for nephew in person.children:
                        if nephew.person.gender=='male':
                            Nephews.append(Person(nephew.person.name, nephew.person.firstName, nephew.person.lastName))
        if Brothers:
            for brother in Brothers:
                person=getPerson(brother.id)
                if person.children:
                    for nephew in person.children:
                        if nephew.person.gender=='male':
                            Nephews.append(Person(nephew.person.name, nephew.person.firstName, nephew.person.lastName))
    
    if Nephews:
        print("Nephews:")
        for n in Nephews:
            print("\t{} {}".format(n.name, n.lastName))
    else:
        print("\tNo nephews.")
    
def showNieces(person):
    """
    A function that prints a person's nieces.
    """
    Sisters=[]
    Brothers=[]
    Nieces=[]
    Sisters=findSisters(person)
    Brothers=findBrothers(person)
    if Sisters or Brothers:
        if Sisters:
            for sister in Sisters:
                person=getPerson(sister.id)
                if person.children:
                    for nephew in person.children:
                        if nephew.person.gender=='female':
                            Nieces.append(Person(nephew.person.name, nephew.person.firstName, nephew.person.lastName))
        if Brothers:
            for brother in Brothers:
                person=getPerson(brother.id)
                if person.children:
                    for nephew in person.children:
                        if nephew.person.gender=='female':
                            Nieces.append(Person(nephew.person.name, nephew.person.firstName, nephew.person.lastName))
    
    if Nieces:
        print("Nieces:")
        for n in Nieces:
            print("\t{} {}".format(n.name, n.lastName))
    else:
        print("\tNo nieces.")

def showSiblingsInLaw(person):
    """
    A function that prints a person's siblings in law.
    """
    SiblingsInLaw=[]
    if person.spouses:
        for spouse in person.spouses:
            if findSisters(spouse.person) or findBrothers(spouse.person):
                for sis in findSisters(spouse.person):
                    s=getPerson(sis.id)
                    SiblingsInLaw.append(Person(s.name, s.firstName, s.lastName))
                for bro in findBrothers(spouse.person):
                    b=getPerson(bro.id)
                    SiblingsInLaw.append(Person(b.name, b.firstName, b.lastName))

    if SiblingsInLaw:
        print("Siblings In Law:")
        for n in SiblingsInLaw:
            print("\t{} {}".format(n.name, n.lastName))
    else:
        print("\tNo Siblings In Law.")

    

def displayPersonData(personId,  debug = False):
    family_tree_model = getFamilyTreeModel()
    found = False
    for person in family_tree_model.persons:
        if person.name == personId:
            print("\n{} {}".format(person.firstName, person.lastName))
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
    print("2 - children")
    print("3 - sisters")
    print("4 - brothers")
    print("5 - brothers and sisters")
    print("6 - grandparents")
    print("7 - grandchildren")
    print("8 - aunts")
    print("9 - uncles")
    print("10 - sisters in law")
    print("11 - brother in law")
    print("12 - nephews")
    print("13 - nieces")
    print("14 - siblings in law")

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
                showChildren(person)
            if choise == "3":
                showSisters(person)
            if choise == "4":
                showBrothers(person)
            if choise == "5":
                showBrothersAndSisters(person)
            if choise == "6":
                showGrandparents(person)
            if choise == "7":
                showGrandchildren(person)
            if choise == "8":
                showAunts(person)
            if choise == "9":
                showUncles(person)
            if choise == "10":
                showSistersInLaw(person)
            if choise == "11":
                showBrothersInLaw(person)
            if choise == "12":
                showNephews(person)
            if choise == "13":
                showNieces(person)
            if choise == "14":
                showSiblingsInLaw(person)

    if not found:
        print("The peson {} doesn't exist in this family!".format(personId))

def printParent(p, c):
    if p.gender:
        if p.gender == "male":
            return print("{} {} is father of {} {}".format(p.firstName, p.lastName, c.firstName, c.lastName))
        else:
            return print("{} {} is mother of {} {}".format(p.firstName, p.lastName, c.firstName, c.lastName))
    else:
        return print("{} {} is parent of {} {}".format(p.firstName, p.lastName, c.firstName, c.lastName))

def checkIfParent(p, c):
    if c.parent1:
        if c.parent1.name == p.name:
            printParent(p, c)
            return True
    if c.parent2:
        if c.parent2.name == p.name:
            printParent(p, c)
            return True
    return False

def printChild(c, p):
    if c.gender:
        if c.gender == "male":
            return print("{} {} is son of {} {}".format(c.firstName, c.lastName, p.firstName, p.lastName))
        else:
            return print("{} {} is daughter of {} {}".format(c.firstName, c.lastName, p.firstName, p.lastName))
    else:
        return print("{} {} is child of {} {}".format(c.firstName, c.lastName, p.firstName, p.lastName))

def checkIfChild(c, p):
    if c.parent1:
        if c.parent1.name == p.name:
            printChild(c, p)
            return True
    if c.parent2:
        if c.parent2.name == p.name:
            printChild(c, p)
            return True
    return False

def checkIfBrotherOrSister(p1, p2):
    #dohvati bracu i sestre osobe p2
    brothersAndSisters = findBrothersAndSisters(p2)
    if brothersAndSisters:
        for bns in brothersAndSisters:
            person = getPerson(bns.id)
            if(person.name == p1.name):
                if p1.gender:
                    if p1.gender == "male":
                        print("{} {} is brother of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                    else:
                        print("{} {} is sister of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                else:
                    print("{} {} is brother/sister of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                return True
    return False

def checkIfBrotherOrSisterInLaw(p1, p2):
    brothersAndSisters = findBrothersAndSisters(p2)
    if brothersAndSisters:
        for bns in brothersAndSisters:
            person = getPerson(bns.id)
            if person.spouses:
                for ps in person.spouses:    
                    if ps.person.name == p1.name: 
                        if p1.gender:
                            if p1.gender == "male":
                                print("{} {} is brother-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                            else:
                                print("{} {} is sister-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                        else:
                            print("{} {} is brother/sister in law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                        return True
    return False

def checkIfSiblingInLaw(p1, p2):
    #get spouses of  p2
    #foreach spouse
    if p2.spouses:
        for sp in p2.spouses:
            brothersAndSistersOfSpouse = findBrothersAndSisters(sp.person)
            if brothersAndSistersOfSpouse:
                for bns in brothersAndSistersOfSpouse:
                    person = getPerson(bns.id)
                    if person.name == p1.name: 
                        print("{} {} is sibling-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                        return True
    return False

def printGrandParent(gp, p):
    if gp.gender:
        if gp.gender == "male":
            return print("{} {} is grandfather of {} {}".format(gp.firstName, gp.lastName, p.firstName, p.lastName))
        else:
            return print("{} {} is grandmother of {} {}".format(gp.firstName, gp.lastName, p.firstName, p.lastName))
    return print("{} {} is grandparent of {} {}".format(gp.firstName, gp.lastName, p.firstName, p.lastName))


def checkIfGrandparent(p1, p2):
    #get parents parent
    if p2.parent1:
        if p2.parent1.parent1:
            if p2.parent1.parent1.name == p1.name:
                printGrandParent(p1, p2)
                return True
        if p2.parent1.parent2:
            if p2.parent1.parent2.name == p1.name:
                printGrandParent(p1, p2)
                return True
    if p2.parent2:
        if p2.parent2.parent1:
            if p2.parent1.parent1.name == p1.name:
                printGrandParent(p1, p2)
                return True
        if p2.parent2.parent2:
            if p2.parent1.parent2.name == p1.name:
                printGrandParent(p1, p2)
                return True
    return False

def printGrandChildren(gc, p):
    if gc.gender:
        if gc.gender == "male":
            return print("{} {} is grandson of {} {}".format(gc.firstName, gc.lastName, p.firstName, p.lastName))
        else:
            return print("{} {} is granddaughter of {} {}".format(gc.firstName, gc.lastName, p.firstName, p.lastName))
    return print("{} {} is grandchild of {} {}".format(gc.firstName, gc.lastName, p.firstName, p.lastName))

def checkIfGrandchildren(p1, p2):
    if p1.parent1:
        if p1.parent1.parent1:
            if p1.parent1.parent1.name == p2.name:
                printGrandChildren(p1, p2)
                return True
        if p1.parent1.parent2:
            if p1.parent1.parent2.name == p2.name:
                printGrandChildren(p1, p2)
                return True
    if p1.parent2:
        if p1.parent2.parent1:
            if p1.parent1.parent1.name == p2.name:
                printGrandChildren(p1, p2)
                return True
        if p1.parent2.parent2:
            if p1.parent1.parent2.name == p2.name:
                printGrandChildren(p1, p2)
                return True
    return False

def printUncleOrAunt(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return print("{} {} is uncle of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
        else :
            return print("{} {} is aunt of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
    return print("{} {} is uncle/aunt of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))

def checkIfUncleOrAunt(p1, p2):
    if p2.parent1:
        auntsAndUncles = findBrothersAndSisters(p2.parent1)
        if auntsAndUncles:
            for anu in auntsAndUncles:
                person = getPerson(anu.id)
                if person.name == p1.name:
                    printUncleOrAunt(p1,p2)
                    return True
    if p2.parent2:
        auntsAndUncles = findBrothersAndSisters(p2.parent2)
        if auntsAndUncles:
            for anu in auntsAndUncles:
                person = getPerson(anu.id)
                if person.name == p1.name:
                    printUncleOrAunt(p1,p2)
                    return True
    return False

def checkIfNephewOrNiece(p1, p2):
    brothersAndSisters = findBrothersAndSisters(p2)
    if brothersAndSisters:
        for bns in brothersAndSisters:
            person = getPerson(bns.id)
            if person.children:
                for c in person.children:
                    if c.person.name == p1.name:
                        if p1.gender:
                            if p1.gender == "male":
                                print("{} {} is nephew of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                                return True
                            else:
                                print("{} {} is niece of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                                return True
                        else:
                            print("{} {} is nephew/niece of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
                            return True
    return False

def printParenInLaw(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return print("{} {} is father-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
        else:
            return print("{} {} is mother-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
    else:
        return print("{} {} is parent-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))

def checkIfParentInLaw(p1, p2):
    if p2.spouses:
        for spouse in p2.spouses:
            if spouse.person.parent1:
                if spouse.person.parent1.name == p1.name:
                    printParenInLaw(p1, p2)
                    return True
            if spouse.person.parent2:
                if spouse.person.parent2.name == p1.name:
                    printParenInLaw(p1, p2)
                    return True
    return False

def printChildInLaw(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return print("{} {} is son-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
        else:
            return print("{} {} is daughter-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))
    else:
        return print("{} {} is child-in-law of {} {}".format(p1.firstName, p1.lastName, p2.firstName, p2.lastName))

def checkIfChildInLaw(p1, p2):
    if p1.spouses:
        for spouse in p1.spouses:
            if spouse.person.parent1:
                if spouse.person.parent1.name == p2.name:
                    printParenInLaw(p1, p2)
                    return True
            if spouse.person.parent2:
                if spouse.person.parent2.name == p2.name:
                    printParenInLaw(p1, p2)
                    return True
    return False

def getPerson(personId):
    family_tree_model = getFamilyTreeModel()
    for person in family_tree_model.persons:
        if person.name == personId:
            return person

def findRelationship(firstPersonId, secondPersonId):
    firstPerson = getPerson(firstPersonId)
    secondPerson = getPerson(secondPersonId)
    if checkIfParent(firstPerson, secondPerson):
        return
    if checkIfChild(firstPerson, secondPerson):
        return
    if checkIfBrotherOrSister(firstPerson, secondPerson):
        return
    if checkIfBrotherOrSisterInLaw(firstPerson, secondPerson):
        return 
    if checkIfSiblingInLaw(firstPerson, secondPerson):
        return
    if checkIfGrandparent(firstPerson, secondPerson):
        return
    if checkIfGrandchildren(firstPerson, secondPerson):
        return
    if checkIfUncleOrAunt(firstPerson, secondPerson):
        return
    if checkIfNephewOrNiece(firstPerson, secondPerson):
        return
    if checkIfParentInLaw(firstPerson, secondPerson):
        return
    if checkIfChildInLaw(firstPerson, secondPerson):
        return 
    print("We couldn't find relation between {} {} and {} {}".format(firstPerson.firstName, firstPerson.lastName, secondPerson.firstName, secondPerson.lastName))

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
        print("3 - find relationship")
        print("4 - end")
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
                    findNextRelationship = True
                    while findNextRelationship:
                        print("Enter persons:")
                        firstPerson = input()
                        secondPerson = input()
                        if not checkIfPersonExistsInModel(firstPerson) or not checkIfPersonExistsInModel(secondPerson):
                            print("Wrong input!")
                        else:
                            if firstPerson == secondPerson:
                                print("It's the same person")
                            else:
                                findRelationship(firstPerson, secondPerson)
                                print("Press enter to find another relationship or anything to go back")
                                if input() != "":
                                    findNextRelationship = False
                else:
                    if choise == "4":
                        do = False
                    else:
                        print("wrong entry")

