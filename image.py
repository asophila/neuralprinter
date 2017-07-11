from PIL import Image

def fit_image(imagen):
    base = Image.open('base.png')
    base_size = base.size
    base_size_l = (base_size[1], base_size[0])
    img = Image.open(imagen)
    img_size = img.size

    if bg_size[0] < bg_size[1] and base_size != img_size:
        img = img.resize(base_size)
    else if bg_size[0] > bg_size[1] and base_size_l != img_size:
        img = img.resize(base_size_l)

    return img

def printeable_image(imagen, base = True):
    foreground = Image.open('base.png')
    fg_size = foreground.size
    background = fit_image(imagen)
    bg_size = background.size

    if bg_size[0] > bg_size[1]:
        background = background.rotate(90, expand=1)

    if base:
        background.paste(foreground, (0, 0), foreground)
    return background
