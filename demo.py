import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import math
import matplotlib.animation as animation 


global_box_selected = []

def on_press(event):
    if event.inaxes == None:
        print("none")
        # fig.canvas.mpl_disconnect(cid)
        # return
    print("my position:" ,event.button,event.xdata, event.ydata)
    click_box = [event.xdata, event.ydata]
    dis = []
    for i in range(5):
        dis.append(math.sqrt((center_points[9][i][0] - click_box[0])**2 + (center_points[9][i][0] - click_box[0])**2)) 
    dis = np.array(dis)
    # smallest distance
    min_ind = np.where(dis==np.min(dis))[0][0]
    box_selected = top_points[9][min_ind]
    print('top_points:',top_points)
    print('box_selected:',box_selected)

    global_box_selected = box_selected

    # fig.canvas.mpl_disconnect(cid)
    draw = ImageDraw.Draw(im)
    draw.rectangle([box_selected[0], box_selected[1], box_selected[0]+resize_h, box_selected[1]+resize_w], outline=(255, 0, 0))
    print('min_ind:',min_ind)
    plt.imshow(im)
    fig.canvas.draw()

    # cid = fig.canvas.mpl_connect('button_press_event', on_press)

    
    # plt.close()
    # fig = plt.figure()
    # plt.imshow(im)
    # plt.show()

    # for i in range(5):
    #     im.paste(cropedIm, (row1_h[i], row1_w[i]))

    # step 4: compute top k, compared with other cameras    
    

    # step 5: show     
    

    # step 6: select which one  and compute which center, show green boxes    
    

    # reset



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

top_points_l = []
for k in range(5):
    # row1_h = []
    # row1_w = []
    floor_k = []
    row1_w_k = row1_w0 + k*(thelta_h+resize_h)
    for i in range(5):
        # row1_h.append(row1_h0+i*(thelta_w+resize_w))
        # row1_w.append(row1_w_k)  
        floor_k.append([row1_h0+i*(thelta_w+resize_w),row1_w_k])  
    top_points_l.append(floor_k)


##########################################################
# top_points
#


row1_h0 = 825
row1_w0 = 73

top_points_r = []
for k in range(5):
    # row1_h = []
    # row1_w = []
    floor_k = []
    row1_w_k = row1_w0 + k*(thelta_h+resize_h)
    for i in range(5):
        # row1_h.append(row1_h0+i*(thelta_w+resize_w))
        # row1_w.append(row1_w_k)    
        floor_k.append([row1_h0+i*(thelta_w+resize_w),row1_w_k])
    top_points_r.append(floor_k)
    # for i in range(5):
    #     im.paste(cropedIm, (row1_h[i], row1_w[i]))   
top_points = top_points_r + top_points_l


features = np.load('demo-features/features/ch02/features.npy')
fnames = np.load('demo-features/features/ch02/fnames.npy')

top_points_l_rela_path = ['ch03','ch26','ch24','ch30','ch22']  # from floor 5 to floor 1, lift
top_points_r_rela_path = ['ch27','ch16','ch08','ch02','ch18']  # from floor 5 to floor 1, east
top_points_rela_path = top_points_r_rela_path + top_points_l_rela_path

center_points = []
for i in range(10):
    one_floor = []
    for j in range(5):
        one_floor.append([top_points[i][j][0]+resize_h/2, top_points[i][j][1]+resize_w/2])
    center_points.append(one_floor)


print('wgc**************************************************')
# visual 
imgs_path = '/media/wang/mySATA/datasets/supercomputer_choose/PROI-Patch/'+ top_points_l_rela_path[4]
features = np.load('demo-features/features/' + top_points_l_rela_path[4] + '/features.npy')
floor_root = np.load('demo-features/features/' + top_points_l_rela_path[4] + '/fnames.npy')

# step 1: show building

# step 2: show paste floor 1
random_indexes = np.random.choice(floor_root.shape[0], size=5, replace=False)
# im.close()
for i in range(5):
    top = top_points[9][i]
    target_path = imgs_path+'/'+floor_root[random_indexes[i]]
    target = Image.open(target_path)
    target = target.resize((resize_h, resize_w))
    box = [top[0],top[1],top[0]+resize_h,top[1]+resize_w]
    im.paste(target, box)
    # draw = ImageDraw.Draw(im)
    # draw.rectangle([box[0], box[1], box[0]+resize_h, box[1]+resize_w], outline=(255, 0, 0))    
fig = plt.figure()
# plt.imshow(im, animated= True)

# im.show()

# def draw_bb(data_gen):
#     print('Drawing beginning!')
#     box_selected= data_gen
#     draw = ImageDraw.Draw(im)
#     draw.rectangle([box_selected[0], box_selected[1], box_selected[0]+resize_h, box_selected[1]+resize_w], outline=(255, 0, 0))
#     print('Drawing finished!')
#     return draw

# def data_gen():
#     print(' I am in!')
#     return iter(global_box_selected)


# step 3: select which one  and compute which center, show green boxes
# draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0))
# cid = fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_press_event', on_press)
plt.imshow(im)
# ani = animation.FuncAnimation(fig, draw_bb, data_gen, blit=True, interval=20, repeat=False)

# plt.plot()
plt.show()
# plt.hold(True)
# plt.plot()
print('hi, friends!')


