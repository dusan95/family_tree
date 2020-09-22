import click
import os
from textx import generator
from textx import GeneratorDesc
from textx.export import metamodel_export, model_export

class Person(object):
    def __init__(self, id = "", name = "", lastName = ""):
        self.id = id
        self.name = name
        self.lastName = lastName

def generate_html (metamodel, model, output_path, overwrite, debug=False, **custom_args):
    """
    This command transforms *.family files to *.html files (html).
    """
    txt = """
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
        <style>
            table, tr, td {
                border: 1px solid black;
            }
        </style>
    </head>
    <body>

    """
    for query in model.queries : 
        if query.__class__.__name__ == "DisplayDataQuery":
            txt += addPersonDataHTML(query.p)
        #if query.__class__.__name__ == "FindRelationshipQuery":
         #   txt += "<p>" + findRelationship(model, query.p1, query.p2) + "</p>"

    txt += """
    </body>
</html>
    """
    
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.abspath(
        os.path.join(base_dir, "{}.{}".format(base_name, 'html')))
    if overwrite or not os.path.exists(output_file):
        click.echo('-> {}'.format(output_file))
        with open(output_file, "w") as f:
            f.write(txt)
    else:
        click.echo('-- Skipping: {}'.format(output_file))


def addPersonDataHTML(person):
    txt = """
        <table>
    """
    txt += "<th>{} {}</th>".format(person.firstName, person.lastName)
    txt += "<tb>"
    if person.dateOfBirth:
        txt += "<tr><td>Date of birth: </td><td>{}.{}.{}.</td></tr>".format(person.dateOfBirth.day, person.dateOfBirth.month, person.dateOfBirth.year)
    else:
        txt += "<tr><td>Date of birth: </td><td> unknown.</td></tr>"
    if person.spouses:
        txt += "<tr><td>Spouses:</td>"
        for sp in person.spouses:
            if sp.since:
                txt += "<td>{} {}, since {}.{}.{}.</td>".format(sp.person.firstName, sp.person.lastName, sp.since.day, sp.since.month, sp.since.year)
            else:
                txt += "<td>{} {}</td>".format(sp.person.firstName, sp.person.lastName)
        txt += "</tr>"
    if person.parent1 and person.parent2:
        txt += "<tr><td>Parents: </td><td> {} {} </td><td> {} {}</td></tr>".format(person.parent1.firstName, person.parent1.lastName,
        person.parent2.firstName, person.parent2.lastName)
    else:
        if person.parent1:
            txt += "<tr><td>Parent: {} {}</td></tr>".format(person.parent1.firstName, person.parent1.lastName)
        if person.parent2:
            txt += "<tr><td>Parent: {} {}</td></tr>\n".format(person.parent2.firstName, person.parent2.lastName)
    brothersAndSisters = findBrothersAndSisters(person)
    if brothersAndSisters:
        txt += "<tr><td>Brothers and sisters:</td>"
        for bns in brothersAndSisters:
            txt += "<td>{} {}</td>".format(bns.name, bns.lastName)
        txt += "</tr>"
    if person.children:
        txt += "<tr><td>Children:</td>"
        for c in person.children:
            txt += "<td>{} {}</td>".format(c.person.firstName, c.person.lastName)
        txt += "</tr>"
    txt += """ </tb></table><br/> """
    return txt


def getPerson(model, personId):
    for person in model.persons:
        if person.name == personId:
            return person

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

def addPersonData(person):
    txt = "{} {}\n".format(person.firstName, person.lastName)
    if person.dateOfBirth:
        txt += "Date of birth: {}.{}.{}.\n".format(person.dateOfBirth.day, person.dateOfBirth.month, person.dateOfBirth.year)
    else:
        txt += "Date of birth: unknown.\n"
    if person.spouses:
        txt += "Spouses:\n"
        for sp in person.spouses:
            if sp.since:
                txt += "\t{} {}, since {}.{}.{}.\n".format(sp.person.firstName, sp.person.lastName, sp.since.day, sp.since.month, sp.since.year)
            else:
                txt += "\t{} {}\n".format(sp.person.firstName, sp.person.lastName)
    if person.parent1 and person.parent2:
        txt += "Parents: {} {} and {} {}\n".format(person.parent1.firstName, person.parent1.lastName,
        person.parent2.firstName, person.parent2.lastName)
    else:
        if person.parent1:
            txt += "Parent: {} {}\n".format(person.parent1.firstName, person.parent1.lastName)
        if person.parent2:
            txt += "Parent: {} {}\n".format(person.parent2.firstName, person.parent2.lastName)
    brothersAndSisters = findBrothersAndSisters(person)
    if brothersAndSisters:
        txt += "Brothers and sisters:\n"
        for bns in brothersAndSisters:
            txt += "\t{} {}\n".format(bns.name, bns.lastName)
    if person.children:
        txt += "Children:\n"
        for c in person.children:
            txt += "\t{} {}\n".format(c.person.firstName, c.person.lastName)
    return txt

def checkIfParent(p, c):
    if c.parent1:
        if c.parent1.name == p.name:
            return True
    if c.parent2:
        if c.parent2.name == p.name:
            return True
    return False

def checkIfChild(c, p):
    if c.parent1:
        if c.parent1.name == p.name:
            return True
    if c.parent2:
        if c.parent2.name == p.name:
            return True
    return False

def checkIfBrotherOrSister(model, p1, p2):
    brothersAndSisters = findBrothersAndSisters(p2)
    if brothersAndSisters:
        for bns in brothersAndSisters:
            person = getPerson(model, bns.id)
            if(person.name == p1.name):
                return True
    return False

def checkIfSpouse(p1, p2):
    if p2.spouses:
        for sp in p2.spouses:
            if sp.person.name == p1.name:
                return True
    return False
    
def checkIfBrotherOrSisterInLaw(model, p1, p2):
    brothersAndSisters = findBrothersAndSisters(p2)
    if brothersAndSisters:
        for bns in brothersAndSisters:
            person = getPerson(model, bns.id)
            if person.spouses:
                for ps in person.spouses:    
                    if ps.person.name == p1.name: 
                        return True
    return False

def checkIfSiblingInLaw(model, p1, p2):
    if p2.spouses:
        for sp in p2.spouses:
            brothersAndSistersOfSpouse = findBrothersAndSisters(sp.person)
            if brothersAndSistersOfSpouse:
                for bns in brothersAndSistersOfSpouse:
                    person = getPerson(model, bns.id)
                    if person.name == p1.name: 
                        return True
    return False

def checkIfGrandparent(p1, p2):
    if p2.parent1:
        if p2.parent1.parent1:
            if p2.parent1.parent1.name == p1.name:
                return True
        if p2.parent1.parent2:
            if p2.parent1.parent2.name == p1.name:
                return True
    if p2.parent2:
        if p2.parent2.parent1:
            if p2.parent1.parent1.name == p1.name:
                return True
        if p2.parent2.parent2:
            if p2.parent1.parent2.name == p1.name:
                return True
    return False

def checkIfGrandchildren(p1, p2):
    if p1.parent1:
        if p1.parent1.parent1:
            if p1.parent1.parent1.name == p2.name:
                return True
        if p1.parent1.parent2:
            if p1.parent1.parent2.name == p2.name:
                return True
    if p1.parent2:
        if p1.parent2.parent1:
            if p1.parent1.parent1.name == p2.name:
                return True
        if p1.parent2.parent2:
            if p1.parent1.parent2.name == p2.name:
                return True
    return False

def checkIfUncleOrAunt(model, p1, p2):
    if p2.parent1:
        auntsAndUncles = findBrothersAndSisters(p2.parent1)
        if auntsAndUncles:
            for anu in auntsAndUncles:
                person = getPerson(model, anu.id)
                if person.name == p1.name:
                    return True
    if p2.parent2:
        auntsAndUncles = findBrothersAndSisters(p2.parent2)
        if auntsAndUncles:
            for anu in auntsAndUncles:
                person = getPerson(model, anu.id)
                if person.name == p1.name:
                    return True
    return False

def checkIfNephewOrNiece(model, p1, p2):
    brothersAndSisters = findBrothersAndSisters(p2)
    if brothersAndSisters:
        for bns in brothersAndSisters:
            person = getPerson(model, bns.id)
            if person.children:
                for c in person.children:
                    if c.person.name == p1.name:
                            return True
    return False

def checkIfParentInLaw(p1, p2):
    if p2.spouses:
        for spouse in p2.spouses:
            if spouse.person.parent1:
                if spouse.person.parent1.name == p1.name:
                    return True
            if spouse.person.parent2:
                if spouse.person.parent2.name == p1.name:
                    return True
    return False

def checkIfChildInLaw(p1, p2):
    if p1.spouses:
        for spouse in p1.spouses:
            if spouse.person.parent1:
                if spouse.person.parent1.name == p2.name:
                    return True
            if spouse.person.parent2:
                if spouse.person.parent2.name == p2.name:
                    return True
    return False

def printRelationship(p1, p2, relationship):
    return "{} {} is {} of {} {}\n".format(p1.firstName, p1.lastName, relationship, p2.firstName, p2.lastName)

def addParent(p, c):
    if p.gender:
        if p.gender == "male":
            return printRelationship(p,c,"father")
        else:
            return printRelationship(p,c,"mother")
    return printRelationship(p,c,"parent")

def addChild(c, p):
    if c.gender:
        if c.gender == "male":
            return printRelationship(c, p, "son")
        else:
            return printRelationship(c, p, "daughter")
    return printRelationship(c, p, "child")

def addBrotherOrSister(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return printRelationship(p1, p2, "brother")
        else:
            return printRelationship(p1, p2, "sister")
    return printRelationship(p1, p2, "sibling")

def addBrotherOrSisterInLaw(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return printRelationship(p1, p2, "brother-in-law")
        else:
            return printRelationship(p1, p2, "sister-in-law")
    return printRelationship(p1, p2, "sibling-in-law")

def addGrandParent(gp, p):
    if gp.gender:
        if gp.gender == "male":
            return printRelationship(gp, p, "grandfather")
        else:
            return printRelationship(gp, p, "grandmother")
    return printRelationship(gp, p, "grandparent")

def addGrandChildren(gc, p):
    if gc.gender:
        if gc.gender == "male":
            return printRelationship(gc, p, "grandson")
        else:
            return printRelationship(gc, p, "granddaughter")
    return printRelationship(gc, p, "grandchild")

def addUncleOrAunt(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return printRelationship(p1, p2, "uncle")
        else :
            return printRelationship(p1, p2, "aunt")
    return printRelationship(p1, p2, "uncle/aunt")

def addNephewOrNiece(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return printRelationship(p1, p2, "nephew")
        else :
            return printRelationship(p1, p2, "niece")
    return printRelationship(p1, p2, "nephew/niece")

def addParenInLaw(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return printRelationship(p1, p2, "father-in-law")
        else :
            return printRelationship(p1, p2, "mother-in-law")
    return printRelationship(p1, p2, "parent-in-law")

def addChildInLaw(p1, p2):
    if p1.gender:
        if p1.gender == "male":
            return printRelationship(p1, p2, "son-in-law")
        else :
            return printRelationship(p1, p2, "daughter-in-law")
    return printRelationship(p1, p2, "child-in-law")

def findRelationship(model, firstPerson, secondPerson):
    if checkIfParent(firstPerson, secondPerson):
        return addParent(firstPerson, secondPerson)
    if checkIfChild(firstPerson, secondPerson):
        return addChild(firstPerson, secondPerson)
    if checkIfBrotherOrSister(model, firstPerson, secondPerson):
        return addBrotherOrSister(firstPerson, secondPerson)
    if checkIfSpouse(firstPerson, secondPerson):
        return "{} {} is spouse of {} {}\n".format(firstPerson.firstName, firstPerson.lastName, secondPerson.firstName, secondPerson.lastName)
    if checkIfBrotherOrSisterInLaw(model, firstPerson, secondPerson):
        return addBrotherOrSisterInLaw(firstPerson, secondPerson)
    if checkIfSiblingInLaw(model, firstPerson, secondPerson):
        return "{} {} is sibling-in-law of {} {}\n".format(firstPerson.firstName, firstPerson.lastName, secondPerson.firstName, secondPerson.lastName)
    if checkIfGrandparent(firstPerson, secondPerson):
        return addGrandParent(firstPerson, secondPerson)
    if checkIfGrandchildren(firstPerson, secondPerson):
        return addGrandChildren(firstPerson, secondPerson)
    if checkIfUncleOrAunt(model, firstPerson, secondPerson):
        return addUncleOrAunt(firstPerson, secondPerson)
    if checkIfNephewOrNiece(model, firstPerson, secondPerson):
        return addNephewOrNiece(firstPerson, secondPerson)
    if checkIfParentInLaw(firstPerson, secondPerson):
        return addParenInLaw(firstPerson, secondPerson)
    if checkIfChildInLaw(firstPerson, secondPerson):
        return addChildInLaw(firstPerson, secondPerson)
    return "We couldn't find relationship between {} {} and {} {}\n".format(firstPerson.firstName, firstPerson.lastName, secondPerson.firstName, secondPerson.lastName)
                

def generate_relationship_text (metamodel, model, output_path, overwrite, debug=False, **custom_args):
    txt = ""
    for query in model.queries : 
        if query.__class__.__name__ == "DisplayDataQuery":
            txt += addPersonData(query.p)
        if query.__class__.__name__ == "FindRelationshipQuery":
            txt += findRelationship(model, query.p1, query.p2)
        txt +="\n"

    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.abspath(
        os.path.join(base_dir, "{}.{}".format(base_name, 'txt')))
    if overwrite or not os.path.exists(output_file):
        click.echo('-> {}'.format(output_file))
        with open(output_file, "w") as f:
            f.write(txt)
    else:
        click.echo('-- Skipping: {}'.format(output_file))

model_to_html = GeneratorDesc(
    language='family_tree_dsl',
    target='HTML',
    description='Generating HTML visualization from family_tree_dsl',
    generator=generate_html
)

model_query_to_txt = GeneratorDesc(
    language='family_tree_dsl',
    target='txt',
    description='Generating txt from family_tree_dsl query',
    generator=generate_relationship_text
)