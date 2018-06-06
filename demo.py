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
    draw.rectangle([box_selected[0], box_selected[1], box_selected[0]+resize_h, box_selected[1]+resize_w], outline=(0, 255, 0))
    print('min_ind:',min_ind)
    plt.imshow(im)
    fig.canvas.draw()

    # step 4: compute top k, compared with other cameras 
    selected_globle_ind = random_indexes[min_ind]   
    feat = features[selected_globle_ind,:] 
    print('feat.shape:',feat.shape)

    for i in range(9):
        ch = top_points_rela_path[i]
        features_ch = features_dict[ch] 
        
        dis_ch = np.sum((feat - features_ch)**2, axis=1)


        print('(feat - features_ch) shape:',(feat - features_ch).shape)
        print('dis_ch shape:',dis_ch.shape)
        print('dis_ch:',dis_ch)
        print('dis_ch min:',np.min(dis_ch))

        dis_sort = np.argsort(dis_ch, axis=0)
        print('dis_sort shape:',dis_sort.shape)

        for j in range(5):
            ind = dis_sort[j]             ###################################
            img_path = '/media/wang/mySATA/datasets/supercomputer_choose/PROI-Patch/'+ ch +'/'+fnames_dict[ch][ind]
            print('img_path:',img_path)
            search_img = Image.open(img_path)
            search_img = search_img.resize((resize_h, resize_w))
            top = top_points[i][j]
            box = [top[0],top[1],top[0]+resize_h,top[1]+resize_w]
            im.paste(search_img, box)
            draw = ImageDraw.Draw(im)
            draw.rectangle([box[0], box[1], box[0]+resize_h, box[1]+resize_w], outline=(255, 0, 0))              
    plt.imshow(im)
    fig.canvas.draw()


    # step 5: select which one  and compute which center, show green boxes    

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




# top_points_l_rela_path = ['ch03','ch26','ch24','ch30','ch22']  # from floor 5 to floor 1, lift
# top_points_r_rela_path = ['ch27','ch16','ch08','ch02','ch18']  # from floor 5 to floor 1, east

top_points_l_rela_path = ['ch02','ch02','ch02','ch02','ch02']  # from floor 5 to floor 1, lift
top_points_r_rela_path = ['ch02','ch02','ch02','ch02','ch02']  # from floor 5 to floor 1, east

top_points_rela_path = top_points_r_rela_path + top_points_l_rela_path



features_dict = {}  
fnames_dict = {}  
for i in range(9):
    ch = top_points_rela_path[i]
    features_dict[ch] = np.load('demo-features/features/'+ch+'/features.npy')
    fnames_dict[ch] = np.load('demo-features/features/'+ch+'/fnames.npy')


center_points = []
for i in range(10):
    one_floor = []
    for j in range(5):
        one_floor.append([top_points[i][j][0]+resize_h/2, top_points[i][j][1]+resize_w/2])
    center_points.append(one_floor)


print('wgc**************************************************')
# visual 
imgs_path = '/media/wang/mySATA/datasets/supercomputer_choose/PROI-Patch/'+ top_points_l_rela_path[4]
# features = np.load('demo-features/features/' + top_points_l_rela_path[4] + '/features.npy')
# floor_root = np.load('demo-features/features/' + top_points_l_rela_path[4] + '/fnames.npy')

# step 1: show building

# step 2: show paste floor 1
random_indexes = np.random.choice(fnames.shape[0], size=5, replace=False)
# im.close()
for i in range(5):
    top = top_points[9][i]
    target_path = imgs_path+'/'+fnames[random_indexes[i]]
    target = Image.open(target_path)
    target = target.resize((resize_h, resize_w))
    box = [top[0],top[1],top[0]+resize_h,top[1]+resize_w]
    im.paste(target, box)
    draw = ImageDraw.Draw(im)
    draw.rectangle([box[0], box[1], box[0]+resize_h, box[1]+resize_w], outline=(255, 0, 0))    
fig = plt.figure()


# step 3: select which one  and compute which center, show green boxes
fig.canvas.mpl_connect('button_press_event', on_press)
plt.imshow(im)
plt.show()
print('hi, friends!')


