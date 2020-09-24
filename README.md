# family tree
This is an example of a family tree DSL which registers new textX language and generators. 

File family-tree.tx in family_tree_dsl folder contains a grammar of the language. Grammar is written in textX DSL. Model example is given in the file miljkovic.family in tests folder.

# Instalation
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
The tar.gz file is a Source Archive whereas the .whl file is a Built Distribution. Newer pip versions preferentially install built distributions, but will fall back to source archives if needed.

You can use pip to install package from the dist folder:
```
    $ pip install textX_family_tree_dsl-0.0.1-py3-none-any.whl
```
# Usage

Make .family file using family-tree.tx grammar.

To generate txt or HTML file for asked queries from command line or powershell(if you are using Visual Studio Code) run:
```
    $ textx generate *.family --target txt --overwrite
    $ textx generate *.family --target HTML --overwrite
```