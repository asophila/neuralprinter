import base64
import requests
import urllib.request, json 
import os
import sched
import time
s = sched.scheduler(time.time, time.sleep)


def find_next_precess(sc):
    with urllib.request.urlopen("http://practiapinta.me/get_next_to_process.php") as url:
        next_style = json.loads(url.read().decode())
        if next_style and not next_style['error']:
            print('-----------------------------------')
            requests.get('http://practiapinta.me/set_status.php?status=PROCESANDO&id=' + next_style['id'])
            print(str(time.time()), 'procesar imagen', next_style['name'])
            print('-----------------------------------')
            style = next_style['estilo']
            filename = 'process/' + next_style['name'] + next_style['ext']
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(next_style['imagen']))

            path_styled = 'process/' + next_style['name'] + '_' + style + next_style['ext']
            model = 'model/' + style + '.pth'
            #print(model)
            #os.system('python neural_style/neural_style.py eval --content-image ' + filename + ' --model ' + model + ' --output-image ' + path_styled + ' --content-scale 5 --cuda 0')
            #while not os.path.exists(path_styled):
            #    process = True

            #TODO: cambiar por procesada
            url = 'http://practiapinta.me/upload_style.php'
            r = requests.post(url, data={'id': next_style['id'], 'name': next_style['name'] + '_' + style + next_style['ext'], 'imagen': next_style['imagen']})
            print(r.json())
            #os.remove(filename)
            #os.remove(path_styled)
            print('-----------------------------------')
            requests.get('http://practiapinta.me/set_status.php?status=PROCESADO&id=' + next_style['id'])
            print(str(time.time()), 'procesada imagen', next_style['name'])
            print('-----------------------------------')
        else:
            print(str(time.time()), 'no hay más por procesar')
        # do your stuff
        s.enter(10, 1, find_next_precess, (sc,))


s.enter(1, 1, find_next_precess, (s,))
s.run()
