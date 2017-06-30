import os

filename = 'process/1498853577.1910024.jpg'
path_styled = filename + '_styled.jpg'
model = 'fast-neural-style-master/model/mosaic.pth'
os.system('python fast-neural-style-master/neural_style/neural_style.py eval --content-image ' + filename +' --model ' + model +' --output-image ' + path_styled + ' --cuda 0')