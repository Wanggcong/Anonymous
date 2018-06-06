import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import math
import matplotlib.animation as animation 

def mouse_detect(x,y,center_points):
    min_dis = 100000;
    which_camera = -1
    rank_k = -1
    
    for i in range(10): 
        for j in range(5):
            dis = math.sqrt((center_points[i][j][0] - x)**2 + (center_points[i][j][1] - y)**2)
            if dis < min_dis:
                which_camera = 	i
                rank_k = j
                min_dis = dis	
    return which_camera, rank_k

random_indexes=[4,3,4,5,6]
# flag = True
# which_camera = -1
def on_press(event):
    # flag = True
    if event.inaxes == None:
        print("none")
    print("my position:" ,event.button,event.xdata, event.ydata)
    ##################################################################################################################################
    # step 2: select which one  and compute which center, show green boxes
    print('center_points:',center_points)
    which_camera, rank_k = mouse_detect(event.xdata, event.ydata,center_points)
    print('which_camera:',which_camera)
    print('rank_k:',rank_k)
    click_box = [event.xdata, event.ydata]
    # dis = []
    # for i in range(5):
    #     dis.append(math.sqrt((center_points[9][i][0] - click_box[0])**2 + (center_points[9][i][0] - click_box[0])**2)) 
    # dis = np.array(dis)
        

    # if flag:
        # smallest distance
        # min_ind = np.where(dis==np.min(dis))[0][0]
    min_ind = rank_k
    top_selected = top_points[which_camera][min_ind]
    box_selected = [top_selected[0],top_selected[1],top_selected[0]+resize_h,top_selected[1]+resize_w]
    # print('top_points:',top_points)
    # print('box_selected:',box_selected)    

    # select one candicate
    draw = ImageDraw.Draw(im)
    draw.rectangle(box_selected, outline=(0, 255, 0))
    # print('min_ind:',min_ind)
    plt.imshow(im)
    fig.canvas.draw()    
    # global which_camera
    if which_camera == 9:
        global random_indexes
        selected_globle_ind = random_indexes[min_ind]   
        feat = features[selected_globle_ind,:] 
        # print('feat.shape:',feat.shape)

        ##################################################################################################################################
        # step 3: show paste floor 1
        # global random_indexes
        random_indexes = [i for i in np.random.choice(fnames.shape[0], size=5, replace=False)]
        random_indexes[min_ind] = selected_globle_ind
        for i in range(5):
            top = top_points[9][i]
            target_path = imgs_path+'/'+fnames[random_indexes[i]]
            target = Image.open(target_path)
            target = target.resize((resize_h, resize_w))
            box = [top[0],top[1],top[0]+resize_h,top[1]+resize_w]
            im.paste(target, box)
            draw = ImageDraw.Draw(im)
            draw.rectangle(box, outline=(0, 0, 255))     
        fig.canvas.draw()    

        ##################################################################################################################################
        # step 4: compute top k, compared with other cameras 
        for i in range(9):
            ch = top_points_rela_path[i]
            features_ch = features_dict[ch] 
            dis_ch = np.sum((feat - features_ch)**2, axis=1)
            dis_sort = np.argsort(dis_ch, axis=0)
            # print('dis_sort shape:',dis_sort.shape)    

            for j in range(5):
                ind = dis_sort[j]             ###################################
                img_path = '/media/wang/mySATA/datasets/supercomputer_choose/PROI-Patch/'+ ch +'/'+fnames_dict[ch][ind]
                # print('img_path:',img_path)
                search_img = Image.open(img_path)
                search_img = search_img.resize((resize_h, resize_w))
                top = top_points[i][j]
                box = [top[0],top[1],top[0]+resize_h,top[1]+resize_w]
                im.paste(search_img, box)
                draw = ImageDraw.Draw(im)
                draw.rectangle(box, outline=(255, 0, 0))              
        # select one candicate
        draw = ImageDraw.Draw(im)
        draw.rectangle(box_selected, outline=(0, 255, 0))
        print('min_ind:',min_ind)
        plt.imshow(im)
        fig.canvas.draw()
        which_camera = -1
    else:
        xxx=2    
    ##################################################################################################################################
    # step 5: select which one  and compute which center, show green boxes    

    ##################################################################################################################################
    # step 6: reset

im_path = '/home/wang/projects/super-computer/school2.JPG';
im = Image.open(im_path)
width, height = im.size
print(im.size, width, height) # 宽高
print(im.format, im.format_description) # 格式，以及格式的详细描述

# (w, h)
row1_h = [200]
row1_w = [600]


resize_h = 38
resize_w = 48


thelta_h = 15
thelta_w = 15


row1_h0 = 180
row1_w0 = 73

top_points_l = []
for k in range(5):
    floor_k = []
    row1_w_k = row1_w0 + k*(thelta_h+resize_h)
    for i in range(5):
        floor_k.append([row1_h0+i*(thelta_w+resize_w),row1_w_k])  
    top_points_l.append(floor_k)

##########################################################
# top_points
row1_h0 = 825
row1_w0 = 73

top_points_r = []
for k in range(5):
    floor_k = []
    row1_w_k = row1_w0 + k*(thelta_h+resize_h)
    for i in range(5): 
        floor_k.append([row1_h0+i*(thelta_w+resize_w),row1_w_k])
    top_points_r.append(floor_k)  
top_points = top_points_r + top_points_l

features = np.load('demo-features/features/ch22/features.npy')
fnames = np.load('demo-features/features/ch22/fnames.npy')
# flag = True


top_points_l_rela_path = ['ch03','ch26','ch24','ch30','ch22']  # from floor 5 to floor 1, lift
top_points_r_rela_path = ['ch27','ch16','ch08','ch02','ch18']  # from floor 5 to floor 1, east

# top_points_l_rela_path = ['ch02','ch02','ch02','ch02','ch02']  # debug
# top_points_r_rela_path = ['ch02','ch02','ch02','ch02','ch02']  # debug

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
imgs_path = '/media/wang/mySATA/datasets/supercomputer_choose/PROI-Patch/'+ top_points_l_rela_path[4]
##################################################################################################################################
# step 0: init
# fig = plt.figure()
fig = plt.figure(figsize=(20,10))
random_indexes = [i for i in np.random.choice(fnames.shape[0], size=5, replace=False)]
# random_indexes[min_ind] = selected_globle_ind
for i in range(5):
    top = top_points[9][i]
    target_path = imgs_path+'/'+fnames[random_indexes[i]]
    target = Image.open(target_path)
    target = target.resize((resize_h, resize_w))
    box = [top[0],top[1],top[0]+resize_h,top[1]+resize_w]
    im.paste(target, box)
    draw = ImageDraw.Draw(im)
    draw.rectangle(box, outline=(0, 0, 255))     
fig.canvas.draw()  

# step 1: prepare mouse click
# fig = plt.figure()        
 
fig.canvas.mpl_connect('button_press_event', on_press)
plt.title('Hello, SYSU iSEE Lab!')
plt.axis('off')
plt.imshow(im)
plt.show()
print('hi, friends!')


