# Family tree
[![MIT licensed](https://img.shields.io/github/license/dusan95/family_tree)](https://img.shields.io)
[![Python version](https://img.shields.io/badge/python-3.8-orange.svg)](https://www.python.org/)

This is an example of a family tree DSL which registers new **textX** language and code generators. 

File family-tree.tx in family_tree_dsl folder contains a grammar of the language. Grammar is written in **textX** DSL. Model example is given in the file **miljkovic.family** in tests folder.

With the help of this language you can easily add family members and search through tree, find relationship between two members or give basic information about specific person, such as date of birth, spouses, parents, children and brothers and sisters.

In tests folder there are two examples how you can use this language. **Proba.py** shows us how to use this language and generators in textX projects by using predefined functions for new languages. **Family-tree.py** is comand line application, where after entering file name you can ask queries for given model: give me basic information about this person, give me relatives of this person or enter two persons and find their relationship. 

This generator supports following relationships: parent, children, sibling, grandparent, grandchildren, spouse, aunt, uncle, nephew, niece, brother-in-law, sister-in-law, parent-in-law, son-in-law, daughter-in-law, sibling-in-law.

## Instalation
To run the language do the following:
```    
    Install Python 3.6.8 or higher
```
Install textX:
```
    $ pip install textX
```
The next step is to generate distribution packages for the package. These are archives that are uploaded to the Package Index and can be installed by pip. Make sure that you have the latest version of setuptools and wheel installed.
```
    $ python -m pip install --user --upgrade setuptools wheel
```
Now run this command from the same directory where setup.py is located:
```   
    $ python setup.py sdist bdist_wheel
```
This command should output a lot of text and once completed should generate two files in the dist directory:
```    
    dist/
        textX_family_tree_dsl-0.0.1-py3-none-any.whl
        textX_family_tree_dsl-0.0.1.tar.gz
```
The tar.gz file is a Source Archive whereas the .whl file is a Built Distribution. 

You can use pip to install package from the dist folder:
```
    $ pip install textX_family_tree_dsl-0.0.1-py3-none-any.whl
```
Newer pip versions preferentially install built distributions, but will fall back to source archives if needed.
## Usage

Make .family file using family-tree.tx grammar.

To generate txt or HTML file for asked queries from command line or powershell(if you are using Visual Studio Code) run:
```
    $ textx generate *.family --target txt --overwrite
    $ textx generate *.family --target HTML --overwrite
```

## License

MIT

## Python versions

Tested for 3.8
