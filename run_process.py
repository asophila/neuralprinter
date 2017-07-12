import base64
import json
import os
import requests
import sched
import time
import urllib.request

import image

def find_next_process(sc):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get('http://pinta.bicubi.co/get_next_to_process.php', headers=headers)

        if r.status_code == 200:
            next_style = r.json()
            if next_style and not next_style['error']:
                print('-----------------------------------')
                r = requests.post('http://pinta.bicubi.co/set_status.php', data={'id': next_style['id'], 'status': 'PROCESANDO'}, headers=headers)
                print(str(time.time()), 'procesando imagen', next_style['name'])
                print('-----------------------------------')

                model = 'model/' + next_style['estilo'] + '.pth'
                #print(model)

                style = next_style['estilo']
                # guardar imagen para procesar
                filename = 'process/' + next_style['name'] + next_style['ext']
                with open(filename, "wb") as fh:
                    fh.write(base64.b64decode(next_style['imagen']))
                # ajustar
                image.fit_image(filename).save(filename)

                # procesar imagen
                path_styled = 'process/' + next_style['name'] + '_' + next_style['estilo'] + next_style['ext']           
                os.system('python neural_style/neural_style.py eval --content-image ' + filename + ' --model ' + model + ' --output-image ' + path_styled + ' --cuda 1')
                while not os.path.exists(path_styled):
                    process = True
                # styled con marco
                #if next_style['evento'] != 'CL':
                image.printeable_image(path_styled).save(path_styled)

                #TODO: cambiar por procesada
                #imagen = filename
                imagen = path_styled
                files = {'file': open(imagen, 'rb')}
                r = requests.post('http://pinta.bicubi.co/upload_style.php',
                    files=files,
                    data={'id': next_style['id'], 'name': next_style['name'] + '_' + next_style['estilo'] + next_style['ext']},
                    headers=headers)
                #print(r.json())

                # borrar imagenes
                #os.remove(filename)
                #os.remove(path_styled)

                print('-----------------------------------')
                r = requests.post('http://pinta.bicubi.co/set_status.php', data={'id': next_style['id'], 'status': 'PROCESADO'}, headers=headers)
                print(str(time.time()), 'procesada imagen', next_style['name'])
                print('-----------------------------------')
            else:
                print(str(time.time()), 'no hay más por procesar')

        else:
            print(str(time.time()), 'Error al recibir respuesta desde el servidor')

    except:
        print('Error red?')
    # do your stuff
    s.enter(10, 1, find_next_process, (sc,))

if not os.path.exists('process/'):
    os.mkdir('process')

s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, find_next_process, (s,))
s.run()
