import db
#import print_windows as printer
import print_linux as printer

import os
import sched
import time
s = sched.scheduler(time.time, time.sleep)

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

s.enter(1, 1, find_next_print, (s,))
s.run()
