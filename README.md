
# Git Quick Reference Document

Repository of reference document (the "cheat sheet") for
[Git Quick Reference](https://github.com/easyintent/quickref)
android application.
It is written in XML to make it easier to edit and validate.

## XML Structure

The [quickref.xml](quickref.xml) document is pretty
much self explainatory. RELAX NG schema describing valid
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
    - Contains zero or more `item`
    - Items directly under `quickref` tag are top level categories
- Item must have an `id` with unique UUID value
    - Id is unique for entire document, it can be generated using `uuidgen`
    - Once id assigned to item, it must not changed
        - Otherwise it would break saved favorite references
- Item must have `title` and `summary` for describing itself
- Item must have either
    - `command` to be written in the console
    - `list` of zero or more reference items


## Packaging to Application

Current application only accept reference document as
[SQLite](http://sqlite.org/) database with full text search `fts4`.
The XML document must be converted to SQLite database
before included in the application. Use simple python
script `mkquickref.py` in this repository for conversion.

### Required Programs

Below programs are required for conversion

- [Python 3.x](http://python.org/), for running `mkquickref.py` itself
- [GNU Make](https://www.gnu.org/software/make/), for executing `Makefile`
- [Xmllint](http://xmlsoft.org/), for validating XML

Consult distribution package manager to install
these programs. If you are using Windows,
it is easier to run under [Cygwin](http://cygwin.com/)
or [MSYS2](http://msys2.github.io/).
Running mkquickref.py directly is possible, but the script expect
valid xml input, hence it rely on xmllint validation.

### Converting XML to SQLite Database

After required programs installed, just run

    $ make

If conversion done without error, `quickref.sqlite` will be
generated on the same directory.

Go to android git quick reference application project,
copy `quickref.sqlite` to the
[`assets`](https://github.com/easyintent/quickref/tree/master/app/src/main/assets)
folder and increase database version number in the `version.properties` file.
Build and run the application.

# License

Licensed under same license as the
[android application](https://github.com/easyintent/quickref).
