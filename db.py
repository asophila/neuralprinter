# -*- coding: utf-8 -*-

import os
import sqlite3
import time

    
def createDB():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
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
def insert_image(usuario, nombre, ext, imagen, estilo, timestamp = ''):
    _timestamp = timestamp if timestamp != '' else time.time()
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
        conn.commit()
        conn.close()
    return

def insert_style(image_style_id, imagen, timestamp = ''):
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

def insert_style1(image_style_id, imagen, timestamp = ''):
    _timestamp = timestamp if timestamp != '' else time.time()

    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Update a row of data
    c.execute('''UPDATE image_style SET
                timestamp = ?,
                ext = ?,
                image = ?,
                status = ?
                WHERE id = ?''',
                (_timestamp, 'jpg', sqlite3.Binary(imagen), 'PROCESADO', image_style_id))
    conn.commit()
    conn.close()
    return

def update_style(image_style_id, status, timestamp = ''):
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

def get_style_print(imagen_id, timestamp = ''):
    _timestamp = timestamp if timestamp != '' else time.time()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Update a row of data
    c.execute('SELECT image, ext, timestamp FROM image_style WHERE id = ?', (imagen_id,))
    ablob, ext, afile = c.fetchone()
    filename = str(afile) + '.' + ext
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    conn.close()
    return filename

def list_images():
    # usar con precaucion con db grande
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Do this instead
    c.execute('SELECT id, user, name FROM image ORDER BY id DESC')
    images = c.fetchall()
    #print(len(images))
    for image in images:
        print('Image:', image[2], 'Upload by:', image[1])

        c.execute('SELECT id, style, status FROM image_style WHERE image_id=?', (image[0],))
        style_images = c.fetchall()
        for style in style_images:
            print('\t(ID:', str(style[0]) + ')','Style:', style[1], '[' + style[2] + ']')      

    conn.close()
    return

database = 'database.db'
if not os.path.exists(database):
    createDB()

#insert_image('gsalazar', 'practia', 'jpg', 'practia.jpg', 'mosaic')
#list_images()
#insert_style(1, 'practia_mosaic.jpg')
#list_images()
#get_style_print(1)