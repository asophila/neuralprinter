# -*- coding: utf-8 -*-

import os
import sqlite3
import time
from PIL import Image


def createDB():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Create table codes
    c.execute('''CREATE TABLE code(
                    id INTEGER PRIMARY KEY ASC,
                    key TEXT,
                    status INTEGER,
                    image_style_id INTEGER REFERENCES image_style(id)
                    )''')

    # Create table image
    # status: [ ]
    c.execute('''CREATE TABLE image(
                    id INTEGER PRIMARY KEY ASC,
                    user TEXT,
                    name TEXT,
                    timestamp REAL,
                    ext TEXT,
                    image BLOB,
                    status TEXT,
                    error_message TEXT
                    )''')

    # Create table image_style
    # style: ['mosaic', '']
    # status: ['A_PROCESAR', 'PROCESANDO', 'PROCESADO', 'IMPRIMIENDO', 'IMPRESO', 'ERROR']
    c.execute('''CREATE TABLE image_style(
                    id INTEGER PRIMARY KEY ASC,
                    image_id INTEGER REFERENCES image(id),
                    timestamp REAL,
                    style TEXT,
                    ext TEXT,
                    image BLOB,
                    status INTEGER,
                    error_message TEXT
                    )''')

    # Save (commit) the changes
    conn.commit()
    conn.close()
    return

# imagen es la ruta del archivo


def insert_image(usuario, nombre, ext, imagen, estilo, code, timestamp=''):
    if not valid_code(code):
        return False, 'El código ya ha sido usado'

    _timestamp = timestamp if timestamp != '' else time.time()

    #bmp = Image.open(imagen)
    #bmp = bmp.resize((1366, 768))
    #bmp.save(imagen, 'JPEG')

    with open(imagen, 'rb') as input_file:
        ablob = input_file.read()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Insert a row of data
        c.execute('''INSERT INTO image(user, name, timestamp, ext, image, status)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                  (usuario, nombre, _timestamp, ext, sqlite3.Binary(ablob), ''))
        image_id = c.lastrowid

        c.execute('''INSERT INTO image_style(image_id, timestamp, style, status)
                        VALUES (?, ?, ?, ?)''',
                  (image_id, _timestamp, estilo, 'A_PROCESAR'))
        image_style_id = c.lastrowid

        c.execute('''UPDATE code SET status = 1, image_style_id = ?
                        WHERE key = ?''',
                  (image_style_id, code))

        conn.commit()
        conn.close()
    return True, ''


def insert_style(image_style_id, imagen, timestamp=''):
    _timestamp = timestamp if timestamp != '' else time.time()
    with open(imagen, 'rb') as input_file:
        ablob = input_file.read()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Update a row of data
        c.execute('''UPDATE image_style SET
                    timestamp = ?,
                    ext = ?,
                    image = ?,
                    status = ?
                    WHERE id = ?''',
                  (_timestamp, 'jpg', sqlite3.Binary(ablob), 'PROCESADO', image_style_id))
        conn.commit()
        conn.close()
    return


def get_next_process():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        'SELECT id, style, image_id FROM image_style WHERE status = "A_PROCESAR" ORDER BY id ASC')
    images = c.fetchall()
    # print(images)
    if len(images) > 0:
        conn.close()
        return images[0]

    conn.close()
    return None


def get_next_print():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(
        'SELECT id FROM image_style WHERE status = "PROCESADO" ORDER BY id ASC')
    images = c.fetchall()
    # print(images)
    if len(images) > 0:
        conn.close()
        return images[0]

    conn.close()
    return None


def update_style(image_style_id, status, timestamp=''):
    _timestamp = timestamp if timestamp != '' else time.time()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Update a row of data
    c.execute('''UPDATE image_style SET
                timestamp = ?,
                status = ?
                WHERE id = ?''',
              (_timestamp, status, image_style_id))
    conn.commit()
    conn.close()
    return


def get_style_print(imagen_style_id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Update a row of data
    c.execute(
        'SELECT image, ext, timestamp FROM image_style WHERE id = ?', (imagen_style_id,))
    ablob, ext, afile = c.fetchone()
    filename = 'print/' + str(afile) + '.' + ext
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    conn.close()
    return filename


def get_image_process(imagen_id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Update a row of data
    c.execute(
        'SELECT image, ext, timestamp FROM image WHERE id = ?', (imagen_id,))
    ablob, ext, afile = c.fetchone()
    filename = 'process/' + str(afile) + '.' + ext
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    conn.close()
    return filename


def generate_codes(num_codes):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Do this instead
    c.execute('SELECT key FROM code')
    codes = c.fetchall()

    i = 0
    while i < num_codes:
        code = len(codes) + 1
        if code not in codes:
            c.execute('''INSERT INTO code(key, status)
                        VALUES (?, ?)''',
                      (code, 0))
            conn.commit()
            i += 1
            c.execute('SELECT key FROM code')
            codes = c.fetchall()
    conn.close()
    return


def valid_code(code):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Do this instead
    c.execute('SELECT status FROM code WHERE key = ?', (code,))
    _code = c.fetchone()
    if _code and _code[0] == 0:
        conn.close()
        return True
    conn.close()
    return False


def list_codes():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Do this instead
    c.execute('SELECT * FROM code ORDER BY id ASC')
    codes = c.fetchall()
    for code in codes:
        print('Key:', code[1], 'Status:', code[2])
        if code[2] > 0:
            c.execute(
                'SELECT image_id FROM image_style WHERE id = ?', (code[3],))
            img_style = c.fetchone()
            c.execute('SELECT name FROM image WHERE id = ?', (img_style[0],))
            img = c.fetchone()
            print('\timage:', img[0])

    conn.close()
    return


def list_images():
    # usar con precaucion con db grande
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Do this instead

    c.execute('SELECT id, user, name FROM image ORDER BY id ASC')
    images = c.fetchall()
    # print(len(images))
    for image in images:
        print('Image:', image[2], 'Upload by:', image[1])

        c.execute(
            'SELECT id, style, status FROM image_style WHERE image_id=?', (image[0],))
        style_images = c.fetchall()
        for style in style_images:
            print('\t(ID:', str(style[0]) + ')',
                  'Style:', style[1], '[' + style[2] + ']')

    conn.close()
    return


database = 'database.db'
if not os.path.exists(database):
    createDB()

if not os.path.exists('process'):
    os.mkdir('process/')

if not os.path.exists('print'):
    os.mkdir('print/')

#print(insert_image('gsalazar', 'practia', 'jpg', 'images/practia.jpg', 'mosaic', 1))

#list_images()
