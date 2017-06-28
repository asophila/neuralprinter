#/usr/bin/python3
import os

printer = '-P EPSON-L475-Series '

def print_image(image_path, printer = ''):
    print('IMPRIMIENDO')
    os.system('lpr ' + printer + image_path)
    os.remove(image_path)
