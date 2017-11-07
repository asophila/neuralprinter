#/usr/bin/python3
import os

def print_image(filename, print_image = False):
    if print_image:
        os.system('lp ' + filename)

    return
