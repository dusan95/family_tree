from textx import metamodel_for_language
from os.path import join, dirname, isfile
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx import generator_for_language_target


data_dsl_mm = metamodel_for_language('family_tree_dsl')
this_folder = dirname(__file__)

def main(debug = False):
    metamodel_export(data_dsl_mm, join(this_folder, 'family-tree_meta.dot'))
    family_tree_model = data_dsl_mm.model_from_file(join(this_folder, "miljkovic.family"))
    model_export(family_tree_model, join(this_folder, 'family-tree.dot'))
    family_tree_to_txt = generator_for_language_target('family_tree_dsl', 'txt')
    family_tree_to_txt(data_dsl_mm, family_tree_model,this_folder,True)
    family_tree_to_html = generator_for_language_target('family_tree_dsl', 'html')
    family_tree_to_html(data_dsl_mm, family_tree_model,this_folder,True)

if __name__ == '__main__':
    main()