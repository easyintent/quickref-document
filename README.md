
# Git Quick Reference Document

This is repository of reference document 
for android application "Git Quick Reference".

## XML Structure

The [quickref.xml](quickref.xml) document is
pretty much self explainatory.
Here is sniplet of the XML document

    <quickref>
        <item id="UUID for this category">
            <title>Title of this category</title>
            <summary>Quick description of this category</summary>
            <list>
                <item id="UUID for this item">
                    <title>Title of this item</title>
                    <summary>Quick description of this item</summary>
                    <command>the git command to be written in console</command>
                </item>
            </list>
        </item>
    </quickref>


- Top level tag is `quickref`
    - Contains zero more `item`
    - Each item directly below `quickref` is top level category
- Item must have an `id` with unique UUID value
    - Id is unique for entire document, can be generated using `uuidgen`
    - Once id assigned to item, it must not changed
        - Otherwise it would break bookmark references
- Item must have `title` and `summary` for describing itself
- Item may have `command` to be written in console
- Item may have `list` of more detailed reference items

The complete XML schema can be found in the [quickref.rng](quickref.rng).

## Packaging to Application

Current application only accept reference document as
SQLite database with full text search `fft4` for faster text search.
So the XML document must be converted to SQLite database
before included in the application. Use simple python
script `mkquickref.py` in this repository for conversion.

### Required Program

Below programs are required for conversion

- Python 3.x, for running `mkquickref.py` itself
- GNU Make, for executing `Makefile`
- Xmllint, for validating XML

Consult distribution package manager to install
these programs. If you are using MS Windows,
it is easier to run under Cygwin or msys2.

### Compiling XML to SQLite Database

After required programs installed, just run

    $ make

If conversion done without error, `quickref.sqlite` will be
generated on the same directory.

Browse android git quick reference application project,
copy `quickref.sqlite` to the `assets` folder and increase
database version number in the `version.properties` file.
Build and run the application.
