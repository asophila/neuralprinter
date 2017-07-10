import base64
import os
import requests
import sched
import time

import send_email as sender

####################################################
# completar estos campos de acuerdo al ambiente y evento
save_images = True
print_os = 'Windows'
evento = ''
####################################################

if print_os == 'Windows':
    print('imprimir Windows')
    import print_windows as printer
else:
    print('imprimir Linux')
    import print_linux as printer

s = sched.scheduler(time.time, time.sleep)

def find_next_print(sc):
    continuar = True

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get('http://pinta.bicubi.co/get_next_to_print.php?evento=' + evento, headers=headers)

    if r.status_code == 200:
        next_print = r.json()
        if next_print and not next_print['error']:
            print('-----------------------------------')
            r = requests.post('http://pinta.bicubi.co/set_status.php', data={'id': next_print['id'], 'status': 'IMPRIMIENDO'}, headers=headers)
            print(str(time.time()), 'imprimiendo imagen', next_print['name'])
            print('-----------------------------------')

            # guardar imagen a imprimir
            filename = 'print/' + str(time.time()) + '_' + next_print['name'] + next_print['ext']
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(next_print['imagen']))

            # enviar por email
            sender.email([next_print['correo']], [filename], next_print['body_correo'])

            # windows
            codigo = next_print['codigo']
            imprimir = True if codigo else False
            printer.print_image(filename, print_image = imprimir)

            # borrar imagenes
            if not save_images:
                os.remove(filename)

            print('-----------------------------------')
            r = requests.post('http://pinta.bicubi.co/set_status.php', data={'id': next_print['id'], 'status': 'IMPRESO'}, headers=headers)
            print(str(time.time()), 'impresa imagen', next_print['name'])
            print('-----------------------------------')
        else:
            print(str(time.time()), next_print['message'])
            if 'evento' in next_print['message']:
                continuar = False

    else:
        print(str(time.time()), 'Error al recibir respuesta desde el servidor')
    # do your stuff
    s.enter(10, 1, find_next_print, (sc,))


s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, find_next_print, (s,))
s.run()
