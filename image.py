# https://github.com/kylefox/python-image-orientation-patch
from PIL import Image, ImageFile

# PIL's Error "Suspension not allowed here" work around:
# s. http://mail.python.org/pipermail/image-sig/1999-August/000816.html
ImageFile.MAXBLOCK = 1024*1024

# The EXIF tag that holds orientation data.
EXIF_ORIENTATION_TAG = 274

# Obviously the only ones to process are 3, 6 and 8.
# All are documented here for thoroughness.
ORIENTATIONS = {
    1: ("Normal", 0),
    2: ("Mirrored left-to-right", 0),
    3: ("Rotated 180 degrees", Image.ROTATE_180),
    4: ("Mirrored top-to-bottom", 0),
    5: ("Mirrored along top-left diagonal", 0),
    6: ("Rotated 90 degrees", Image.ROTATE_270),
    7: ("Mirrored along top-right diagonal", 0),
    8: ("Rotated 270 degrees", Image.ROTATE_90)
}

def fix_orientation(img, save_over=False):
    """
    `img` can be an Image instance or a path to an image file.
    `save_over` indicates if the original image file should be replaced by the new image.
    * Note: `save_over` is only valid if `img` is a file path.
    """
    path = None
    if not isinstance(img, Image.Image):
        path = img
        img = Image.open(path)
    elif save_over:
        raise ValueError("You can't use `save_over` when passing an Image instance.  Use a file path instead.")
    try:
        orientation = img._getexif()[EXIF_ORIENTATION_TAG]
    except (TypeError, AttributeError, KeyError):
        raise ValueError("Image file has no EXIF data.")
    if orientation in [3,6,8]:
        degrees = ORIENTATIONS[orientation][1]
        img = img.transpose(degrees)
        if save_over and path is not None:
            try:
                img.save(path, quality=95, optimize=1)
            except IOError:
                # Try again, without optimization (PIL can't optimize an image
                # larger than ImageFile.MAXBLOCK, which is 64k by default).
                # Setting ImageFile.MAXBLOCK should fix this....but who knows.
                img.save(path, quality=95)
        return (img, degrees)
    else:
        return (img, 0)

###############

def get_size(base_size, img_size):
    new_size = img_size

    if img_size[0] < img_size[1]:
        new_size = (img_size[0], int((img_size[0] * base_size[1]) / base_size[0]))
    elif img_size[0] > img_size[1]:
        new_size = (int((img_size[1] * base_size[1]) / base_size[0]), img_size[1])

    return new_size, int(abs(img_size[1] - new_size[1])/2)

def fit_image(imagen):
    base = Image.open('base.png')
    base_size = base.size

    img = Image.open(imagen)
    img_size = img.size

    try:
        img, degrees = fix_orientation(img)
        if degrees == 0 and img_size[0] > img_size[1]:
            img = img.rotate(90, expand=1)
        #print('rotate', degrees)
    except:
        error = True
        #print('no exif image', imagen)
        if img_size[0] > img_size[1]:
            img = img.rotate(90, expand=1)

    img_size = img.size

    if img_size[0] != img_size[1]:
        new_size = get_size(base_size, img_size)
        #print(img_size, '>', new_size[0], ':', new_size[1])
        if new_size[1] > 0:
            #print('cambiar relacion', imagen)
            if (img_size[0]/img_size[1]) > (base_size[0]/base_size[1]):                
                # fill black
                #img = img.crop((0, -new_size[1], new_size[0][0], new_size[0][1] - new_size[1]))
                # fill white or personalizable
                bg = Image.new('RGBA', new_size[0], (255,255,255,255))
                bg.paste(img, (0, new_size[1]))
                img = bg
                # end fill
            else:
                img = img.crop((0, new_size[1], new_size[0][0], new_size[0][1]))
            img = img.resize(base_size)
        elif img_size != new_size[0]:
            #print('resize')
            img = img.resize(base_size)
    else:
        #print('add top-bottom')
        new_size = get_size(base_size, img_size)
        # fill black        
        #img = img.crop((0, -new_size[1], new_size[0][0], new_size[0][1] - new_size[1]))
        # fill white or personalizable
        bg = Image.new('RGBA', new_size[0], (255,255,255,255))
        bg.paste(img, (0, new_size[1]))
        img = bg
        # end fill
        img = img.resize(base_size)

    return img

def printeable_image(imagen, base = True):
    foreground = Image.open('base.png')
    fg_size = foreground.size
    background = Image.open(imagen)
    bg_size = background.size

    if bg_size[0] > bg_size[1]:
        background = background.rotate(90, expand=1)

    if base:
        background.paste(foreground, (0, 0), foreground)
    return background
