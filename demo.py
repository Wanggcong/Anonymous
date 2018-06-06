#!/usr/bin/python3
# -*- coding:UTF-8 -*-
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
cam_status = [0,0,0,0,0,0,0,0,0,1]
# flag = True
# which_camera = -1
def on_press(event):
    if event.inaxes == None:
        print("单击超出范围，请重新单击鼠标...")
    # print("请单击鼠标选择待查询图片或依次选择目标ID...")
    # print("my position:" ,event.button,event.xdata, event.ydata)
    ##################################################################################################################################
    # step 2: select which one  and compute which center, show green boxes
    # print('center_points:',center_points)
    which_camera, rank_k = mouse_detect(event.xdata, event.ydata,center_points)
    global cam_status
    cam_status[which_camera] = 1
    # print('which_camera:',which_camera)
    # print('rank_k:',rank_k)
    click_box = [event.xdata, event.ydata]
    min_ind = rank_k
    top_selected = top_points[which_camera][min_ind]
    box_selected = [top_selected[0],top_selected[1],top_selected[0]+resize_h,top_selected[1]+resize_w] 

    # select one candicate
    draw = ImageDraw.Draw(im)
    draw.rectangle(box_selected, outline=(0, 255, 0))
    # print('min_ind:',min_ind)
    plt.imshow(im)
    fig.canvas.draw()    
    # global which_camera
    if which_camera == 9:
        # print('待查询图片. 请依次选择目标ID ...')
        cam_status = [0,0,0,0,0,0,0,0,0,1]
        global random_indexes
        selected_globle_ind = random_indexes[min_ind]   
        feat = features[selected_globle_ind,:] 

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
        # step 4: compute top k, compared with other cameras, select which one  and compute which center, show green boxes   
        for i in range(9):
            ch = top_points_rela_path[i]
            features_ch = features_dict[ch] 
            dis_ch = np.sum((feat - features_ch)**2, axis=1)
            dis_sort = np.argsort(dis_ch, axis=0)
            # print('dis_ch[dis_sort[0]] :',dis_ch[dis_sort[0]])  
            # if dis_ch[dis_sort[0]] < 0.5:
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
                if dis_ch[ind] < 0.5:
                    draw.rectangle(box, outline=(255, 0, 0))              
                else:
                    # draw.rectangle(box, fill=(255, 0, 0))  
                    draw.rectangle(box, outline=(255, 0, 0))  
                    draw.line([(top[0],top[1]),(top[0]+resize_h,top[1]+resize_w)], fill=(255, 0, 0))  
                    draw.line([(top[0],top[1]+resize_w),(top[0]+resize_h,top[1])], fill=(255, 0, 0))  
        # select one candicate
        draw = ImageDraw.Draw(im)
        draw.rectangle(box_selected, outline=(0, 255, 0))
        # print('min_ind:',min_ind)
        plt.imshow(im)
        fig.canvas.draw()
        which_camera = -1
    # else:
    #     print('继续选择目标ID或者重新更新待查询图片 ...')   
    ##################################################################################################################################
    # step 5: Visual trajectories
    x_l1,x_l2 = 600, 118
    x_r1,x_r2 = 760, 100
    cam_l0 = [x_l1,x_l2,x_l1+10,x_l2+10]
    cam_r0 = [x_r1,x_r2,x_r1+10,x_r2+10]

    cam_l_thelta = 40
    cam_r_thelta = 40
    
    draw = ImageDraw.Draw(im)
    for i in range(5):
        if cam_status[i+5] == 1:
            draw.ellipse((cam_l0[0],cam_l0[1]+i*cam_l_thelta,cam_l0[2],cam_l0[3]+i*cam_l_thelta), fill=(0, 255, 0))
        else:
            draw.ellipse((cam_l0[0],cam_l0[1]+i*cam_l_thelta,cam_l0[2],cam_l0[3]+i*cam_l_thelta), fill=(255, 0, 0))
    for i in range(5):    
        if cam_status[i] == 1:
            draw.ellipse((cam_r0[0],cam_r0[1]+i*cam_r_thelta,cam_r0[2],cam_r0[3]+i*cam_r_thelta),fill = (0, 255, 0))    
        else:
            draw.ellipse((cam_r0[0],cam_r0[1]+i*cam_r_thelta,cam_r0[2],cam_r0[3]+i*cam_r_thelta),fill = (255, 0, 0))  
    plt.imshow(im)
    fig.canvas.draw()
    if which_camera != 9 and which_camera != -1:
        print('锁定目标ID在摄像机：'+str(which_camera))
    # else:
    #     print('请进一步筛选和确定目标ID...')
    print('筛选目标ID或更新待查询ID ...') 
    print('*******************************************************')
im_path = '/home/wang/projects/super-computer/school2.JPG';
im = Image.open(im_path)
width, height = im.size
# print(im.size, width, height) # 宽高
# print(im.format, im.format_description) # 格式，以及格式的详细描述

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
fig = plt.figure(figsize=(12,8))
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
# plt.text(0,420,"Blue: query",fontsize=15,verticalalignment="top",horizontalalignment="left",color='b')
# plt.text(0,460,"Red: searched",fontsize=15,verticalalignment="top",horizontalalignment="left",color='r')
# plt.text(0,500,"Green: confirmed!",fontsize=15,verticalalignment="top",horizontalalignment="left",color='g')
plt.text(100,460,"Blue: query",fontsize=15,verticalalignment="top",horizontalalignment="left",color='b')
plt.text(500,460,"Red: searched",fontsize=15,verticalalignment="top",horizontalalignment="left",color='r')
plt.text(900,460,"Green: confirmed!",fontsize=15,verticalalignment="top",horizontalalignment="left",color='g')
plt.axis('off')
plt.imshow(im)


print('初始化完成。请单击鼠标选择待查询图片（蓝色框） ...')
plt.show()
print('Welcome back!')


