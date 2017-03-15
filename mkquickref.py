#!/usr/bin/python3

import sys
import sqlite3
import uuid
import xml.etree.ElementTree as et

# The reference table
#
CREATE_TABLE = '''
    CREATE TABLE quickref (
        id TEXT UNIQUE,
        parent_id TEXT,
        leaf INT,
        priority INT,
        title TEXT,
        summary TEXT,
        command TEXT
    )
'''

# Inserting list of dictionary
#
INSERT_ROWS = '''
    INSERT INTO quickref
        (id, parent_id, leaf, priority, title, summary, command)
    VALUES 
        (:id, :parent_id, :leaf, :priority, :title, :summary, :command)
'''

# Virtual table using full text search for faster text search
#
CREATE_SEARCH_TABLE = '''
    CREATE VIRTUAL TABLE quicksearch
        USING fts4(content=quickref, title, summary, command)
'''

REBUILD_INDEX = '''
    INSERT INTO quicksearch(quicksearch) VALUES('rebuild')
'''

# Convert quickref XML file to SQLite database
#
def quickref_xml_to_sqlite(src_file, dst_file):
    quickref_tree = quickref_xml_to_tree(src_file)
    quickref_tree_to_sqlite(quickref_tree, dst_file)


# Parse XML quickref file to dictionary tree.
#
def quickref_xml_to_tree(xml_file):
    xml_tree = et.parse(xml_file)
    xml_root = xml_tree.getroot()
    
    root_tag = xml_root.tag

    if root_tag != 'quickref':
        raise ValueError(
            "Root element must be 'quickref', "
            "found '{0}'".format(root_tag))

    items = []

    for xml_child in xml_root:
        item = _parse_xml_item(xml_child)
        items.append(item)

    return {root_tag: items}


# Convert quickref dictionary tree to sqlite table.
#
def quickref_tree_to_sqlite(quickref_tree, sqlite_file):

    items = quickref_tree['quickref']

    conn = sqlite3.connect(sqlite_file)    
    cur = conn.cursor()

    cur.execute(CREATE_TABLE)
    cur.execute(CREATE_SEARCH_TABLE)

    # flatten the dictionary tree
    rows = _flatten_item(items, None)

    # rows is now list of flat dictionary 
    # [{'id':, 'parent_id':, ...}].
    #
    cur.executemany(INSERT_ROWS, rows)

    # build full text search table
    cur.execute(REBUILD_INDEX)

    conn.commit()
    conn.close()


# Convert single <item> tag to dictionary, recursively.
#
def _parse_xml_item(xml_item):

    item = {}
    item['id'] = xml_item.get('id')

    children = []

    for i in xml_item:
        if i.tag == 'list':
            for j in i:
                sub_item = _parse_xml_item(j)
                children.append(sub_item)
        else:
            item[i.tag] = i.text

    if children:
        item['list'] = children

    return item


# Flatten children of items, recursively.
#
def _flatten_item(items, parent_id):

    priority = 1
    rows = []

    for item in items:

        unique_id = item.get('id')
        title = item.get('title')
        summary = item.get('summary')
        command = item.get('command')
        children = item.get('list')

        # make sure it is valid UUID
        unique_id = str(uuid.UUID(unique_id))

        row = {
            'id': unique_id,
            'parent_id': parent_id,
            'leaf': children is None,
            'priority': priority,
            'title': title,
            'summary':  summary,
            'command':  command
        }

        rows.append(row)

        # order by item location in the item list
        priority = priority + 1

        # flatten children
        if children is not None:
            children_rows = _flatten_item(children, unique_id)
            rows.extend(children_rows)

    return rows

if __name__ == '__main__':

    if len(sys.argv) == 3:
        src_file = sys.argv[1]
        dst_file = sys.argv[2]
        quickref_xml_to_sqlite(src_file, dst_file)
    else:
        print('usage: mkquickref.py input.xml output.sqlite')
