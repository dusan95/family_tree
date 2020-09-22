import os
import textx.scoping.tools as tools
from textx import metamodel_from_file, TextXSyntaxError, language
from textx.export import metamodel_export, model_export


@language('family_tree_dsl', '*.family')
def family_tree_dsl():
    """
    An example DSL for simple types definition
    """
    current_dir = os.path.dirname(__file__)
    p = os.path.join(current_dir, 'family-tree.tx')
    family_tree_mm = metamodel_from_file(p, global_repository=True)

    return family_tree_mm