import logging
import os
import sqlite3
import sys
import re

#TODO rewrite this to not look like terrible shit

def new_tags(line):
    global tags, title

    results = REGEX_TAG.findall(line)
    if results:
        logging.debug('found tags: {}'.format(results))
        tags += results
        return True
    return False

def fill_db(fp):
    global cursor, tags, title, paragraph_id

    head = True
    content = ''
    first_line = True
    for line in fp:
        if first_line:
            first_line = False
            continue
        if new_tags(line):
            head = False
            if content:
                cursor.execute(
                    'INSERT INTO help(id, content) VALUES (?, ?)',
                    (paragraph_id, content)
                )
                paragraph_id += 1
            for tag in tags:
                cursor.execute(
                    'INSERT INTO tags(name, help_id) VALUES (?, ?)',
                    (tag[1:-1], paragraph_id)
                )
                tags = []
            content = ''
        elif not head:
            content += line
            if content.strip() == '':
                content = ''

if __name__ == '__main__':

    path = sys.argv[1] if len(sys.argv) > 1 else '/usr/share/vim/vim81/doc'

    REGEX_TAG=re.compile('(\*\S*\*)')
    paragraph_id = 0
    tags = []

    try:
        os.remove('vim_doc.db')
    except FileNotFoundError:
        pass
    connection = sqlite3.connect('vim_doc.db')
    cursor = connection.cursor()
    with open('init.sql') as f:
        cursor.executescript(f.read())

    for file in os.listdir(path):
        with open(os.path.join(path, file)) as f:
            fill_db(f)

    connection.commit()
    connection.close()

    logging.info('done')
