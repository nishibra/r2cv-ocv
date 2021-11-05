#!/usr/bin/env python
#! -*- coding: utf-8 -*-
#Created on Thu Oct 19 07:06:36 2017
# @author: Nishimura @ AiRRC
import sys
import numpy as np
import cv2
import rclpy
#
w=320
h=240
#
def find_color(img,ryb):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    mask = np.zeros(h.shape, dtype=np.uint8)
    if ryb==0:
    #RED/GREEN
        mask[((h>0) & (h < 13)) & (s > 128)] = 255
        #mask[((h>50) & (h < 90)) & (s > 128)] = 255
    elif ryb==1:
    #Yellow
        mask[((h>45) & (h < 48)) & (s > 128)] = 255
    else:
    #Blue
        mask[((h>150) & (h < 200)) & (s > 128)] = 255
    kernel = np.ones((7,7),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours,aa= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
    cv2.imshow('mask',mask)
    rects = []
    xmax=0
    ymax=0
    rmax=0
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
        print ('counter=',rect[0])
        #find biggest one
        nn=0
        rr=0
        for rect in rects:
            nn=nn+1
            if rr<rect[2]:
                rr=rect[2]
                xmax=int(rect[0]+rect[2]/2)
                ymax=int(rect[1]+rect[3]/2)
                rmax=int(rect[2]/2)
            cv2.circle(img, (int(rect[0]+rect[2]/2),int(rect[1]+rect[3]/2)), int(rect[2]/2), (0, 0, 255), thickness=1)
            cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=1)
            cv2.putText(img, str(nn), tuple(rect[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=1)
        
    return img,xmax,ymax,1
#
def cal_point_dist(xr,yr,xl,yl):
    global w,h
    xd=(-xl+xr)
    yd=(-yl+yr)
    print (xd,yd)
    if yd<10 and yd>-10 and xd != 0:
        z=1300.0/xd
        print('Z=',z)
    else:
        z=0
    if z<0 or z>200:
        z=0
    print('z1=',z)
    x=z*((xl+xr)/2-w/2)/120
    y=-z*((yl+yr)/2-h/2)/120
    print(x,y,z)
    return int(x),int(y),int(z)
#
def main():
    capR = cv2.VideoCapture(0)
    capR.set(3,w)
    capR.set(4,h)
    capR.set(5,15)
    capR.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    capL = cv2.VideoCapture(2)
    capL.set(3,w)
    capL.set(4,h)
    capL.set(5,15)
    capL.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not capR.isOpened():
        raise Exception ('camera is not found')
    while (capR.isOpened()):
        ret, frameR = capR.read()
        ret, frameL = capL.read()
        rflag=0
        if ret == True:
            frameR,xr,yr,rflag=find_color(frameR,0)
            cv2.circle(frameR,(xr,yr),10, (0, 0, 255), thickness=-1)
            cv2.imshow('frameRf',frameR)
            if rflag==1:
                frameL,xl,yl,lflag=find_color(frameL,0)
                cv2.imshow('frameL',frameL)
                if (lflag==1) and (-xl+xr)!=0:
                    print(xr,yr,xl,yl)  
                    x,y,z=cal_point_dist(xr,yr,xl,yl)
                    print ("p.c.=",x,y,z)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        else:
            break
    capR.release()
    capL.release()
    cv2.destroyAllWindows()
#
if __name__ == "__main__":
    main()

