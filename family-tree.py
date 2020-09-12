from os.path import join, dirname, isfile
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

def main(fileName, personId, debug=False):
    # Get meta-model from language description and export it to dot   GRAMATIKA
    family_tree_meta = metamodel_from_file(join(this_folder, 'family-tree.tx'), debug=debug)
    metamodel_export(family_tree_meta, join(this_folder, 'family-tree_meta.dot'))

    # Instantiate model and export it to dot      FAJL KOJI SE UCITAVA
    family_tree_model = family_tree_meta.model_from_file(join(this_folder, fileName))
    model_export(family_tree_model, join(this_folder, 'family-tree.dot'))

    for person in family_tree_model.persons:
        if person.name == personId:
            print("{} {}'s parents are {} {} and {} {}".format(person.firstName, person.lastName,
            person.parent1.firstName, person.parent1.lastName, person.parent2.firstName, person.parent2.lastName))

    #for command in family_tree_model.commands:
     #   if command.__class__.__name__ == "QueryParentCommand":
      #      print("{} is parent of {}".format(command.p.firstName, command.c.firstName))
       #     #ako je klasa parent komanda treba napraviti vezu
        #if command.__class__.__name__ == "GenderCommand":
         #   print("{} {} is {}".format(command.person.firstName, command.person.lastName, command.gender))
        #if command.__class__.__name__ == "StatusCommand":
         #   print("{} {} is {}".format(command.person.firstName, command.person.lastName, command.status))

def displayPersonData(fileName, personId,  debug = False):
    # Get meta-model from language description and export it to dot   GRAMATIKA
    family_tree_meta = metamodel_from_file(join(this_folder, 'family-tree.tx'), debug=debug)
    metamodel_export(family_tree_meta, join(this_folder, 'family-tree_meta.dot'))

    # Instantiate model and export it to dot      FAJL KOJI SE UCITAVA
    family_tree_model = family_tree_meta.model_from_file(join(this_folder, fileName))
    model_export(family_tree_model, join(this_folder, 'family-tree.dot'))
    found = False
    for person in family_tree_model.persons:
        if person.name == personId:
            if person.dateOfBirth is not None :
                print("{} {} is born on {}.{}.{}.".format(person.firstName, person.lastName, person.dateOfBirth.day, person.dateOfBirth.month, person.dateOfBirth.year))
            else:
                print("{} {}.".format(person.firstName, person.lastName))
            if person.spouses is not None :
                for sp in person.spouses:
                    print("Spouse {} {}".format(sp.spouse.firstName, sp.spouse.lastName))
            found = True
    if not found:
        print("The peson {} doesn't exist!".format(personId))

def chooseRelationship(fileName):
    print("Choose relationship:")
    print("1 - parents")
    choise = input()
    if(choise == "1"):
        print("Unesite osobu")
        personId = input()
        main(fileName, personId)

if __name__ == '__main__':
    this_folder = dirname(__file__)
    do = True
    fileName = ""
    while do:
        print("Please enter filename")
        fileName = input()
        if isfile(join(this_folder, fileName)):
            #proveriti da model li odgovara gramatici
            do = False
        else:
            print("wrong")
    do = True
    while do:
        print("Choose one of the options: ")
        print("1 - show person data")
        print("2 - query ")
        print("3 - end")
        choise = input()
        if(choise == "1"):
            print("Enter person name") 
            personId = input()
            displayPersonData(fileName, personId)
        else:
            if(choise == "2"):
                chooseRelationship(fileName)
            else:
                if(choise == "3"):
                    do = False
                else:
                    print("wrong entry")

