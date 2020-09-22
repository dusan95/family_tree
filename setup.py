from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="family_tree_dsl", 
    version="0.0.3",
    author="Dusan Miljkovic",
    author_email="dusanmiljkovic_95@hotmail.com",
    description="A small family-tree dsl and generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dusan95/family_tree",
    packages=find_packages(),
    package_data={'': ['*.tx']},
    install_requires=["textx"],
    dependency_links=['https://github.com/textX/textX'],
    entry_points={
        'textx_languages': [
            'family_tree_dsl = family_tree_dsl:family_tree_dsl',
        ],
        'textx_generators' : [
            'family_tree_gen_html = family_tree_gen.generators:model_to_html',
            'family_tree_gen_txt = family_tree_gen.generators:model_query_to_txt',
        ],
    },
)