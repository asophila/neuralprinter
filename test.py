import os

_model = 'mosaic'
filename = 'process/1498855984.789918.jpg'

path_styled = filename + '_' + _model + '.jpg'
model = 'fast-neural-style-master/model/' + _model + '.pth'

os.system('python fast-neural-style-master/neural_style/neural_style.py eval --content-image ' + filename +' --model ' + model +' --output-image ' + path_styled + ' --cuda 0')