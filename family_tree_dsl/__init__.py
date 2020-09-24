import os
from textx import metamodel_from_file, language

@language('family_tree_dsl', '*.family')
def family_tree_dsl():
    """
    A meta-language for family-tree definition
    """
    current_dir = os.path.dirname(__file__)
    p = os.path.join(current_dir, 'family-tree.tx')
    family_tree_mm = metamodel_from_file(p, global_repository=True)

    return family_tree_mm