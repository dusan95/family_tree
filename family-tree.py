from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

class Person(object):
    def __init__(self, name = "", lastName = "", dateOfBirth = "", alive = "", gender = "",
     parent1 = "", parent2 = "", supose = "" ):
        self.name = name
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.alive = alive
        self.gender = gender
        self.parent1 = parent1
        self.parent2 = parent2
        self.supose = supose



def main(debug=False):

    this_folder = dirname(__file__)

    # Get meta-model from language description and export it to dot
    family_tree_meta = metamodel_from_file(join(this_folder, 'family-tree.tx'), debug=debug)
    metamodel_export(family_tree_meta, join(this_folder, 'family-tree_meta.dot'))

    # Instantiate model and export it to dot
    family_tree_model = family_tree_meta.model_from_file(join(this_folder, 'family-tree.rbt'))
    model_export(family_tree_model, join(this_folder, 'family-tree.dot'))

    for person in family_tree_model.persons:
        print("{} {} is born on {}.{}.{}.".format(person.firstName, person.lastName, person.dateOfBirth.day, person.dateOfBirth.month, person.dateOfBirth.year))

    for command in family_tree_model.commands:
        if command.__class__.__name__ == "ParentCommand":
            print("{} is parent of {}".format(command.p.firstName, command.c.firstName))
            #ako je klasa parent komanda treba napraviti vezu
        if command.__class__.__name__ == "GenderCommand":
            print("{} {} is {}".format(command.person.firstName, command.person.lastName, command.gender))
        if command.__class__.__name__ == "StatusCommand":
            print("{} {} is {}".format(command.person.firstName, command.person.lastName, command.status))

    #print("{} is parent of {}".format(parent.name, child.name))
    #print("{} is {}, and {} is {}".format(parent.name, parent.gender, child.name, child.gender))

if __name__ == '__main__':
    list = []
    list.append( Person() )
    main()
