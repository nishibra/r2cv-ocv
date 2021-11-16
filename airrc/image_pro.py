#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by T.Nishimura
# 2020.10.22
#
import cv2
import numpy as np
import time
import math 
#
def read_img():
  img = cv2.imread('image.png')
  return (img)
#
def write_img(nameimg,img):
  cv2.imwrite(nameimg,img)
#
def resize_img(img,w,h):
  ##resize--
  img = cv2.resize(img,(w,h))
  return (img)
#
def zoom_img(img,zo):#zo=0,1,2,3,4
  h,w,c=img_size(img)
  #trim
  img_zoom = img[int(h*zo/10):int(h-h*zo/10), int(w*zo/10):int(w-w*zo/10)]
  return (img_zoom)
#
def rotat(img,ang):
  h,w,c=img_size(img)
  m = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1)
  im_roto = cv2.warpAffine(img, m, (w,h))
  return(im_roto)
  #
def edge_pro(img):
  ##edge--
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (5,5), 1)
  #cv2.imshow('frame0',gray)
  edges = cv2.Canny(gray,3,20,apertureSize = 3)
  kernel = np.ones((3,3),np.uint8)
  #kernel = np.ones((2,2),np.uint8)
  edge = cv2.dilate(edges,kernel,iterations = 1)
  #cv2.imwrite('edges.jpg',edges)
  return(edge)
#
def line_pro(img,edge):
  ##line
  #rhoは直線までの距離, thetaは回転角度
  #threshold は直線を動かして、その直線に乗ってきた点の数
  minLineLength = 150
  maxLineGap = 40
  lines = cv2.HoughLinesP(edge,1,np.pi/180,30,minLineLength,maxLineGap)
  h,w,color=img.shape
  #dislay
  if lines is not None:
    for line in lines:
      x1,y1,x2,y2=line[0]
      cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
  return(img,edge)
#
def circle_pro(img,edge):
#circle dp 解像度2で1/2 minDist 円間距離 param1 小さいとエッジ検出 
#   param2　小さいといろいろ検出 minRadius,maxRadius
  minR=30
  maxR=40
  circles = cv2.HoughCircles(edge,cv2.HOUGH_GRADIENT,
            1,100,param1=1,param2=10,minRadius=minR,maxRadius=maxR)
  #print ('****** min=',minR,'max=',maxR,'circles=',circles)
  if circles is not None:
    # convert (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
      cv2.circle(img, (x, y), r, (0, 255, 0), 2)
  return(img,edge)
#
def draw_circle(img,x,y,r):
  cv2.circle(img, (x, y), r, (0, 255, 0), 2)
#
def imshow_pro(edge,img):
  edge2 = cv2.cvtColor(edge,cv2.COLOR_GRAY2BGR)
  img2=cv2.hconcat([edge2,img])
  put_airrc(img2)
  cv2.imshow('edge',img2)
#
def hcon_img(img1,img2):
  img=cv2.hconcat([img1,img2])
  return(img)
#
def vcon_img(img1,img2):
  img=cv2.vconcat([img1,img2])
  return(img)
#
def graytorgb(img):
  img2 = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
  return(img2)
#
def put_airrc(img):
  cv2.putText(img, "AiRRC", (10,55),0, 1, (0, 0, 255), 1, cv2.LINE_AA)
  return(img)
#
def img_size(img):
  height, width, channels = img.shape[:3]
  return height, width, channels
#--------------------------------------------------
def main():
  print('image processing in python-opencv')
  cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
  cap.set(cv2.CAP_PROP_FPS, 15)
  cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
  while(cap.isOpened()):
    #for x in range(0,2):
    ret, img = cap.read()
    if ret==True:
      img=rotat(img,10)
      img=zoom_img(img,3)
      img=resize_img(img,160,120)
      cv2.imshow('image',img)
      #edge=edge_pro(img)
      #img,edge1=line_pro(img,edge)
      #img,edge2=circle_pro(img,edge)
      #imshow_pro(edge1,img)
      #imshow_pro(edge2,img)
      #time.sleep(0.5)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        print ("quit")
        break
    else:
        print ("no flame")
        break
  cap.release()
  cv2.destroyAllWindows()
#--------------------------------------------------
if __name__ == "__main__":
  main()
