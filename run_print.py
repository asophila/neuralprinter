import base64
import requests
import urllib.request, json 
import send_email as send
import print_windows as printer
#import print_linux as printer

import os
import sched
import time
s = sched.scheduler(time.time, time.sleep)


def find_next_print(sc):
    with urllib.request.urlopen("http://practiapinta.me/get_next_to_print.php") as url:
        next_print = json.loads(url.read().decode())
        if next_print and not next_print['error']:
            print('-----------------------------------')
            requests.get('http://practiapinta.me/set_status.php?status=IMPRIMIENDO&id=' + next_print['id'])
            filename = 'print/' + next_print['name'] + next_print['ext']
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(next_print['imagen']))

            if 'candy' in filename:
                send.email([next_print['correo']], [filename])
            print(str(time.time()), 'imprimir imagen:', filename)
            printer.print_image(filename, False)  # windows
            # printer.print_image(filename) #linux
            requests.get('http://practiapinta.me/set_status.php?status=IMPRESO&id=' + next_print['id'])
            # os.remove(filename)
            print('-----------------------------------')
        else:
            print(str(time.time()), 'no hay más por imprimir')

        # do your stuff
        s.enter(10, 1, find_next_print, (sc,))


s.enter(1, 1, find_next_print, (s,))
s.run()
