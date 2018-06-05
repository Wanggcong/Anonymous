from PIL import Image
import numpy as np

im_path = '/home/wang/projects/super-computer/school2.JPG';
im = Image.open(im_path)
width, height = im.size
# 宽高
print(im.size, width, height)
# 格式，以及格式的详细描述
print(im.format, im.format_description)

# (w, h)
crop_h = 40
crop_w = 55

row1_h = [200]
row1_w = [600]

cropedIm = im.crop((row1_h[0], row1_w[0], row1_h[0]+crop_h, row1_w[0] + crop_w))
# cropedIm.show()


resize_h = 55
resize_w = 40


thelta_h = 5
thelta_w = 5


row1_h0 = 180
row1_w0 = 73

for k in range(5):
    row1_h = []
    row1_w = []
    row1_w_k = row1_w0 + k*(thelta_h+resize_h)
    for i in range(5):
        row1_h.append(row1_h0+i*(thelta_w+resize_w))
        row1_w.append(row1_w_k)    

    for i in range(5):
        im.paste(cropedIm, (row1_h[i], row1_w[i]))





##########################################################

row1_h0 = 825
row1_w0 = 73

for k in range(5):
    row1_h = []
    row1_w = []
    row1_w_k = row1_w0 + k*(thelta_h+resize_h)
    for i in range(5):
        row1_h.append(row1_h0+i*(thelta_w+resize_w))
        row1_w.append(row1_w_k)    

    for i in range(5):
        im.paste(cropedIm, (row1_h[i], row1_w[i]))

features = np.load('demo-features/features/ch02/features.npy')
fnames = np.load('demo-features/features/ch02/fnames.npy')


im.show()