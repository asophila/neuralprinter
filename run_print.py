import base64
import json
import os
import requests
import sched
import time
import urllib.request

import send_email as send
import print_windows as printer
#import print_linux as printer

s = sched.scheduler(time.time, time.sleep)


def find_next_print(sc):
    with urllib.request.urlopen("http://practiapinta.me/get_next_to_print.php") as url:
        next_print = json.loads(url.read().decode())
        if next_print and not next_print['error']:
            print('-----------------------------------')
            r = requests.post('http://practiapinta.me/set_status.php', data={'id': next_print['id'], 'status': 'IMPRIMIENDO'})
            print(str(time.time()), 'imprimiendo imagen', next_print['name'])
            print('-----------------------------------')

            # guardar imagen a imprimir
            filename = 'print/' + next_print['name'] + next_print['ext']
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(next_print['imagen']))

            # enviar por email
            send.email([next_print['correo']], [filename])

            # windows
            printer.print_image(filename, print_image = True)
            # linux
            #printer.print_image(filename) 

            # borrar imagenes
            #os.remove(filename)

            print('-----------------------------------')
            r = requests.post('http://practiapinta.me/set_status.php', data={'id': next_print['id'], 'status': 'IMPRESO'})
            print(str(time.time()), 'impresa imagen', next_print['name'])
            print('-----------------------------------')
        else:
            print(str(time.time()), 'no hay más por imprimir')

        # do your stuff
        s.enter(10, 1, find_next_print, (sc,))


s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, find_next_print, (s,))
s.run()
