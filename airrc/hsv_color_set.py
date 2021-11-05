#!/usr/bin/env python
# -*- coding: utf-8 -*-
# T.Nishimura @ AiRRC
#
import sys
import numpy as np
from subprocess import *
import time
from time import sleep
import datetime
from pytz import timezone
from datetime import timedelta
import cv2
#
w=320
h=240
wh=50
whs=30
hh=h
wv=w+wh
hv=30
hvs=50
xx=int(w/2)
yy=int(h/2)
#
def hsv_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    for x in range(0,20):
         for y in range(0,320):
                 #print y
                 hsv[x, y, 0]=y
                 hsv[x, y, 1]=128
                 hsv[x, y, 2]=128
    bgr_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)
    return bgr_img
#
def find_color(img):
    global xx,yy
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h>yy) & (h<xx)) & (s>50)] = 255
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contour,aa= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mmm=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow('mask2',mmm)
    rects = []
    print (len(contour))
    for contour in contour:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
        #find top1
        nn=0
        for rect in rects:
            nn=nn+1
            cv2.circle(img, (int(rect[0]+rect[2]/2),int(rect[1]+rect[3]/2)), int(rect[2]/2), (0, 0, 255), thickness=1)
            cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=1)
            cv2.putText(img, str(nn), tuple(rect[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=1)
    return img
#
def draw_sq(event,x,y,flags,param):
    global xx,yy
    if event == cv2.EVENT_LBUTTONDOWN:
        if y>66:
            xx=x
        else:
            yy=x
        print ("H=",xx,yy)
#
if __name__ == "__main__":
    cv2.namedWindow('ColorSet')
    cv2.setMouseCallback('ColorSet',draw_sq)
    cap = cv2.VideoCapture(0)
    cap.set(3,w)
    cap.set(4,h)
    #
    titl_img = np.zeros((30,320, 3), np.uint8)
    titl2_img = np.zeros((20,320, 3), np.uint8)
    bar_img = np.zeros((40,320, 3), np.uint8)
    # Title
    cv2.putText(titl_img,"HSV COLOR No.", (60,22),0, 0.6, (250,250,250),1, cv2.LINE_AA)
    cv2.putText(titl_img,"AiRRC", (260,22),0, 0.5, (20,20,220),1, cv2.LINE_AA)
    # Title bar2
    titl2_img=hsv_color(titl2_img)
    while(cap.isOpened()):
        try:
            ret, came_img = cap.read(-1)
        except:
            print ("Camera error")
        #data = cv2.rotate(data, cv2.ROTATE_180)
        cam_img=find_color(came_img)
        #bar
        bar_img = np.zeros((40,320, 3), np.uint8)
        cv2.line(bar_img, (0,15), (319,15), (55,255,30), thickness=1, lineType=cv2.LINE_8)
        cv2.rectangle(bar_img, (xx,5), (xx+1,25), (55,255,255),thickness=-1)
        cv2.rectangle(bar_img, (yy,5), (yy+1,25), (255,255,30),thickness=-1)
        cv2.putText(bar_img,"H1="+str(yy)+" H2="+str(xx), (200,32),0, 0.4, (220,220,220),1, cv2.LINE_AA)

        img2=cv2.vconcat([titl_img,titl2_img,bar_img,came_img])
        cv2.imshow('ColorSet',img2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

