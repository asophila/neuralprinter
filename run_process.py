import db

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
        filename = next_style[2]
        
        path_styled = 'process/' + next_style[3] + '_' + style + next_style[4]
        model = 'model/' + style + '.pth'
        print(model)
        os.system('python neural_style/neural_style.py eval --content-image ' + filename +' --model ' + model +' --output-image ' + path_styled + ' --content-scale 5 --cuda 0')

        while not os.path.exists(path_styled):
            process = True
        
        db.insert_style(next_style[0], path_styled)
        #os.remove(filename)
        os.remove(path_styled)
        print('-----------------------------------')
        db.update_style(next_style[0], 'PROCESADO')
        print(str(time.time()), 'procesada imagen', next_style[0]) 
        print('-----------------------------------')
    else:
        print(str(time.time()), 'no hay más por procesar')
    # do your stuff
    s.enter(20, 1, find_next_precess, (sc,))

s.enter(1, 1, find_next_precess, (s,))
s.run()
