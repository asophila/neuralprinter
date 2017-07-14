import base64
import json
import os
import requests
import sched
import time
import urllib.request

import image

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

###################################################################################################
url = 'http://pinta.bicubi.co'
save_images = True
###################################################################################################

def next_process():
    r = requests.get(url + '/has_next_to_process.php', headers=headers)
    if r.status_code == 200:
        next_style = r.json()
        if next_style:
            if next_style['error']:
                return False, next_style['message']
            # else: download image
            r = requests.get(url + '/get_next_to_process.php', headers=headers)
            if r.status_code == 200:
                next_style = r.json()
                if next_style:
                    if next_style['error']:
                        return False, next_style['message']
                    #####################################
                    # solo 1 caso éxito                 #
                    return True, next_style             #
                    #####################################
            return False, 'Error al descargar imagen'
        return False, 'Error al recibir json'    
    return False, 'Error ' + str(r.status_code)

def upload_image(filename, upload_data):
    files = {'file': open(filename, 'rb')}
    r = requests.post(url + '/upload_style.php',
        files = files,
        data = {
                'id': upload_data['id'],
                'name': upload_data['name'] + '_' + upload_data['estilo'] + upload_data['ext']
                },
        headers = headers)
    #print(r.json())
    return (r.status_code == 200)

def set_status(id, estado):
    print('-----------------------------------')
    r = requests.post(url + '/set_status.php', data={'id': id, 'status': estado}, headers=headers)
    print(str(time.time()), str(id), '> Estado >', estado)
    print('-----------------------------------')
    return

def save_image_to_process(data, fit = False):
    filename = 'process/' + str(time.time()) + '_' + data['name'] + data['ext']
    with open(filename, "wb") as fh:
        fh.write(base64.b64decode(data['imagen']))

    # ajustar
    if fit:
        image.fit_image(filename)
        
    return filename

def process_image(data, model):
    # guardar imagen para procesar
    fit = True
    filename = save_image_to_process(data, fit)
    # procesar imagen
    path_styled = 'process/' + str(time.time()) + '_' + data['name'] + '_' + data['estilo'] + data['ext']           
    os.system('python neural_style/neural_style.py eval --content-image ' + filename + ' --model ' + model + ' --output-image ' + path_styled + ' --cuda 1')
    while not os.path.exists(path_styled):
        process = True

    # styled con marco
    border = (not 'ppm_sm_pd' in filename)# and (data['evento'] == 'CL')
    if border:
        image.printeable_image(path_styled)

    # upload image styled
    print('subir imagen')
    r = upload_image(path_styled, data)

    if not r:
        return False, 'Error al subir la imagen'

    # borrar imagenes
    if not save_images:
        os.remove(filename)
        os.remove(path_styled)

    return True

def find_next_process(sc):
    try:
        next_to_process = next_process()
        if next_to_process[0]:
            next_style = next_to_process[1]
            set_status(next_style['id'], 'PROCESANDO')

            model = 'model/' + next_style['estilo'] + '.pth'
            if os.path.exists(model):
                # procesar imagen
                upload = process_image(next_style, model)
                if upload:
                    set_status(next_style['id'], 'PROCESADO')
                else:
                    set_status(next_style['id'], 'ERROR')
            else:
                set_status(next_style['id'], 'ERROR')
                print('Modelo no válido')
        else:
            print(str(time.time()), next_to_process[1])

    except Exception as ex:
        print('Error', ex)
    # do your stuff
    s.enter(10, 1, find_next_process, (sc,))

###################################################################################################
if not os.path.exists('process/'):
    os.mkdir('process')

s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, find_next_process, (s,))
s.run()
