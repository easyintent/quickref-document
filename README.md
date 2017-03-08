
# Git Quick Reference Document

Repository of reference document for android application
"Git Quick Reference".
This repository is the actual content of that application.
The document is written in XML to make it
easier to edit and validate.

## XML Structure

The [quickref.xml](quickref.xml) document is pretty
much self explainatory. XML schema describing valid
XML document can be found in the [quickref.rng](quickref.rng).
Here is sniplet of the XML document

    <quickref>
        <item id="UUID for this category">
            <title>Title of this category</title>
            <summary>Short description of this category</summary>
            <list>
                <item id="UUID for this item">
                    <title>Title of this item</title>
                    <summary>Short description of this item</summary>
                    <command>The git command to be written in the console</command>
                </item>
            </list>
        </item>
    </quickref>


- Top level tag is `quickref`
    - Contains zero more `item`
    - Each item directly under `quickref` is top level category
- Item must have an `id` with unique UUID value
    - Id is unique for entire document, it can be generated using `uuidgen`
    - Once id assigned to item, it must not changed
        - Otherwise it would break bookmark references
- Item must have `title` and `summary` for describing itself
- Item may have `command` to be written in console
- Item may have `list` of more detailed reference items


## Packaging to Application

Current application only accept reference document as
SQLite database with full text search `fft4`.
The XML document must be converted to SQLite database
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

### Converting XML to SQLite Database

After required programs installed, just run

    $ make

If conversion done without error, `quickref.sqlite` will be
generated on the same directory.

Go to android git quick reference application project,
copy `quickref.sqlite` to the `assets` folder and increase
database version number in the `version.properties` file.
Build and run the application.
