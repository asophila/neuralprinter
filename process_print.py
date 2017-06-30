import os

import db
import print_windows as printer
#import print_linux as printer

print()
print('-----------------------------------')
next_print = db.get_next_print()
if next_print:
    db.update_style(next_print[0], 'IMPRIMIENDO')
    filename = db.get_style_print(next_print[0])
    print('imprimir imagen:', filename)
    printer.printer(filename, True)
    db.update_style(next_print[0], 'IMPRESO')
    # os.remove(filename)
else:
    print('no hay más por imprimir')

print('-----------------------------------')
print()
