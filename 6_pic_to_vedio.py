# -*- coding: utf-8 -*-
import os
import cv2

file_dir = "pic"
file_list = []
for root, dirs, files in os.walk(file_dir):
    for file in files:
        file_list.append(file)
        
video = cv2.VideoWriter("sz_covid19.mp4",cv2.VideoWriter_fourcc("m","p","4","v"),2,(1920,1080))

for i in range(len(file_list)):
    img = cv2.imread("pic/"+file_list[i])
    #print(img.shape)
    img =cv2.resize(img, (1920,1080))
    video.write(img)

video.release()