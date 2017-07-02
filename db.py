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
                    image_id INTEGER REFERENCES image(id)
                    )''')

    # Create table image
    # status: ['A_PROCESAR', 'PROCESANDO', 'PROCESADO', 'IMPRIMIENDO', 'IMPRESO', 'ERROR']
    c.execute('''CREATE TABLE image(
                    id INTEGER PRIMARY KEY ASC,
                    usuario TEXT,
                    ip TEXT,
                    correo TEXT,
                    empresa TEXT,
                    cargo TEXT,
                    estilo TEXT,
                    name TEXT,
                    ext TEXT,
                    imagen BLOB,
                    imagen_style BLOB,
                    timestamp REAL,
                    status TEXT,
                    error_message TEXT
                    )''')

    # Save (commit) the changes
    conn.commit()
    conn.close()
    return

# imagen es la ruta del archivo


def insert_image(info, timestamp=''):
    if not valid_code(info['codigo']):
        return False, 'El código ya ha sido usado'

    _timestamp = timestamp if timestamp != '' else time.time()

    #bmp = Image.open(imagen)
    #bmp = bmp.resize((1366, 768))
    #bmp.save(imagen, 'JPEG')

    with open(info['path'], 'rb') as input_file:
        ablob = input_file.read()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Insert a row of data
        c.execute('''INSERT INTO image(usuario, ip, correo, empresa, cargo, estilo, name, ext, imagen, timestamp, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?)''',
                  (info['usuario'], info['ip'], info['correo'], info['empresa'], info['cargo'], info['estilo'], info['name'], info['ext'], sqlite3.Binary(ablob), _timestamp, 'A_PROCESAR'))
        image_id = c.lastrowid

        c.execute('''UPDATE code SET status = 1, image_id = ?
                        WHERE key = ?''',
                  (image_id, info['codigo']))

        conn.commit()
        conn.close()
    return True, ''


def insert_style(image_id, imagen, timestamp=''):
    _timestamp = timestamp if timestamp != '' else time.time()
    with open(imagen, 'rb') as input_file:
        ablob = input_file.read()
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # Update a row of data
        c.execute('''UPDATE image SET
                    timestamp = ?,
                    imagen_style = ?,
                    status = ?
                    WHERE id = ?''',
                  (_timestamp, sqlite3.Binary(ablob), 'PROCESADO', image_id))
        conn.commit()
        conn.close()
    return


def get_next_process():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    try:
        c.execute(
            'SELECT id, estilo, imagen, ext, timestamp FROM image WHERE status = "A_PROCESAR" ORDER BY id ASC')
        _id, estilo, ablob, ext, afile = c.fetchone()
        if _id > 0:
            filename = 'process/' + str(afile) + ext
            with open(filename, 'wb') as output_file:
                output_file.write(ablob)
            conn.close()
            return _id, estilo, filename, str(afile), ext
    except:
        error = True
    conn.close()
    return None

def get_next_print():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    try:
        c.execute(
            'SELECT id, imagen_style, ext, timestamp FROM image WHERE status = "PROCESADO" ORDER BY id ASC')
        _id, ablob, ext, afile = c.fetchone()
        if _id > 0:
            filename = 'print/' + str(afile) + ext
            with open(filename, 'wb') as output_file:
                output_file.write(ablob)
            conn.close()
            return _id, filename
    except:
        error = True
    conn.close()
    return None


def update_style(image_id, status, timestamp=''):
    _timestamp = timestamp if timestamp != '' else time.time()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Update a row of data
    c.execute('''UPDATE image SET
                timestamp = ?,
                status = ?
                WHERE id = ?''',
              (_timestamp, status, image_id))
    conn.commit()
    conn.close()
    return True

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
    return True

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
                'SELECT name, estilo FROM image WHERE id = ?', (code[3],))
            img = c.fetchone()
            print('\timage:', img[0], '>>', img[1])

    conn.close()
    return True

def list_images():
    # usar con precaucion con db grande
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Do this instead

    c.execute('SELECT id, usuario, name, estilo FROM image ORDER BY id ASC')
    images = c.fetchall()
    # print(len(images))
    for image in images:
        print('Imagen:', image[2], '>>', image[3], 'Upload by:', image[1])

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
