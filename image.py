from PIL import Image

def clean_image(imagen):
    foreground = Image.open('base.png')
    fg_size = foreground.size
    background = Image.open(imagen)
    bg_size = background.size

    #if bg_size[0] > bg_size[1]:
    #    background = background.rotate(90, expand=1)

    if fg_size != bg_size:
        background = background.resize(foreground.size)

    background.paste(foreground, (0, 0), foreground)
    return background
