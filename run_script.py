import db
#import print_windows as printer
import print_linux as printer

import os
import sched
import time
s = sched.scheduler(time.time, time.sleep)


def find_next_precess(sc):
    next_style = db.get_next_process()
    if next_style:
        print('-----------------------------------')
        db.update_style(next_style[0], 'PROCESANDO')
        print(str(time.time()), 'procesar imagen', next_style[0])        
        print('-----------------------------------')

        style = next_style[1]
        image_id = next_style[2]
        # TODO process image
        filename = db.get_image_process(image_id)
        path_styled = filename + '_styled.jpg'
        os.system('python fast-neural-style-master/neural_style/neural_style.py eval --content-image ' + filename +' --model ./fast-neural-style-master/model/mosaic.pth --output-image ' + path_styled + ' --cuda 0')

        while not os.path.exists(path_styled):
            process = True

        db.insert_style(next_style[0], path_styled)
        # os.remove(filename)
        print('-----------------------------------')
        db.update_style(next_style[0], 'PROCESADO')
        print(str(time.time()), 'procesada imagen', next_style[0]) 
        print('-----------------------------------')
    else:
        print(str(time.time()), 'no hay más por procesar')
    # do your stuff
    s.enter(5, 1, find_next_precess, (sc,))


def find_next_print(sc):
    next_print = db.get_next_print()
    if next_print:
        print('-----------------------------------')
        db.update_style(next_print[0], 'IMPRIMIENDO')
        filename = db.get_style_print(next_print[0])
        print(str(time.time()), 'imprimir imagen:', filename)
        printer.print_image(filename)
        db.update_style(next_print[0], 'IMPRESO')
        # os.remove(filename)
        print('-----------------------------------')
    else:
        print(str(time.time()), 'no hay más por imprimir')

    # do your stuff
    s.enter(10, 1, find_next_print, (sc,))


s.enter(1, 1, find_next_precess, (s,))
s.enter(1, 1, find_next_print, (s,))
s.run()
