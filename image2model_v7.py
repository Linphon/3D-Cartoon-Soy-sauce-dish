#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:45:29 2017

@author: morty
"""

from numpy import *
import PIL.Image as image
import numpy as np
modellist = ['solid OpenSCAD_Model']

def loadDataSet(filename):
    data = np.asarray(image.open(filename).convert('L'))
    return data
 
def vector2str(vector):
    return ' '.join([str(i) for i in vector]) 

def write_in(x1,x2,x3,faceVector):
    line = '  facet normal ' + vector2str(faceVector)
    modellist.append(line)
    modellist.append('    outer loop')
    for vector in (x1,x2,x3):
        line = ' '*6 + 'vertex ' + vector2str(vector)
        modellist.append(line)
    modellist.append('    endloop')
    modellist.append('  endfacet')

def normalize(data,gradient,s):
    num_gradient = int(ceil(255/gradient))
    out_data = data.copy()
    for i in range(num_gradient):
        out_data[(data>(i*gradient))*(data<=((i+1)*gradient))] = i
    scale = round((gradient*s/25.5),1)
    out_data = out_data * scale
    return out_data

def normalize2(data):
    m,n = shape(data)
    for i in range(m):
        for j in range(n):
            if ((i==0) or (i==(m-1)) or (j==0) or (j==(n-1))):
                data[i,j] = 0
    return data

def initial_wall(data,scale,height):
    #initial the modellist with four walls and an undersurface
    m,n = shape(data)
    s = scale * 2
    #write_in((0,n,0),(m,n,0),(0,0,0),(0,0,-1))
    #write_in((0,0,0),(m,n,0),(m,0,0),(0,0,-1))
    write_in((-s,n+s,-s),(m+s,n+s,-s),(-s,-s,-s),(0,0,-1))
    write_in((-s,-s,-s),(m+s,n+s,-s),(m+s,-s,-s),(0,0,-1))
    # this is the floor
    
    #write_in((m,0,0),(m,n,0),(m,n,height),(1,0,0))
    #write_in((m,0,height),(m,0,0),(m,n,height),(1,0,0))
    write_in((m+s,-s,-s),(m+s,n+s,-s),(m+s,n+s,height),(1,0,0))
    write_in((m+s,-s,height),(m+s,-s,-s),(m+s,n+s,height),(1,0,0))
    #his is y&z
    #write_in((0,0,height),(0,n,height),(0,0,0),(-1,0,0))
    #write_in((0,0,0),(0,n,height),(0,n,0),(-1,0,0))
    write_in((-s,-s,height),(-s,n+s,height),(-s,-s,-s),(-1,0,0))
    write_in((-s,-s,-s),(-s,n+s,height),(-s,n+s,-s),(-1,0,0))
    #this is y&z
    
    #write_in((0,n,0),(m,n,height),(m,n,0),(0,1,0))
    #write_in((0,n,0),(0,n,height),(m,n,height),(0,1,0))
    write_in((-s,n+s,-s),(m+s,n+s,height),(m+s,n+s,-s),(0,1,0))
    write_in((-s,n+s,-s),(-s,n+s,height),(m+s,n+s,height),(0,1,0))
    #this is x&z
    #write_in((0,0,0),(m,0,0),(m,0,height),(0,-1,0))
    #write_in((0,0,height),(0,0,0),(m,0,height),(0,-1,0))
    write_in((-s,-s,-s),(m+s,-s,-s),(m+s,-s,height),(0,-1,0))
    write_in((-s,-s,height),(-s,-s,-s),(m+s,-s,height),(0,-1,0))
    #this is x&z
    
    write_in((-s,-s,height),(m+s,0,height),(m+s,-s,height),(0,0,1)) 
    write_in((-s,-s,height),(-s,0,height),(m+s,0,height),(0,0,1)) 
    write_in((-s,n,height),(m+s,n+s,height),(m+s,n,height),(0,0,1)) 
    write_in((-s,n,height),(-s,n+s,height),(m+s,n+s,height),(0,0,1)) 
    write_in((-s,0,height),(0,n,height),(0,0,height),(0,0,1)) 
    write_in((-s,0,height),(-s,n,height),(0,n,height),(0,0,1)) 
    write_in((m,0,height),(m+s,n,height),(m+s,0,height),(0,0,1)) 
    write_in((m,0,height),(m,n,height),(m+s,n,height),(0,0,1)) 
    #this is floors

def build_inwall(data,h):
    m,n=shape(data)
    face_vector_yp,face_vector_yn = (0,1,0),(0,-1,0)
    face_vector_xp,face_vector_xn = (1,0,0),(-1,0,0)
    for i in range(m):        
        lh1 = data[i,0]
        write_in((i+1,0,lh1),(i,0,lh1),(i,0,h),face_vector_yp) 
        write_in((i+1,0,lh1),(i,0,h),(i+1,0,h),face_vector_yp) 
        lh2 = data[i,n-1]
        write_in((i,n,lh2),(i+1,n,lh2),(i+1,n,h),face_vector_yn)  
        write_in((i,n,lh2),(i+1,n,h),(i,n,h),face_vector_yn)  
    for j in range(n):
        lh1 = data[0,j]
        write_in((0,j,lh1),(0,j+1,lh1),(0,j+1,h),face_vector_xp) 
        write_in((0,j,lh1),(0,j+1,h),(0,j,h),face_vector_xp) 
        lh2 = data[m-1,j]
        write_in((m,j+1,lh2),(m,j,lh2),(m,j,h),face_vector_xn) 
        write_in((m,j+1,lh2),(m,j,h),(m,j+1,h),face_vector_xn) 

def build_floor(data):
    m,n = shape(data)
    for i in range(m):
        for j in range(n):
            if data[i,j] == 0:
                face_vector = (0,0,1)
                write_in((i,j,0),(i+1,j,0),(i,j+1,0),face_vector)
                write_in((i,j+1,0),(i+1,j,0),(i+1,j+1,0),face_vector)  
                
def build_prop(data):
    m,n = shape(data)
    face_vector_xp,face_vector_xn = (1,0,0),(-1,0,0)
    face_vector_yp,face_vector_yn = (0,1,0),(0,-1,0)
    for i in range(m):
        for j in range(n):
            if data[i,j]:
                if (i-1) >= 0:
                    if data[i,j] > data[i-1,j]:
                        hh = data[i,j] # high height
                        lh = data[i-1,j] # low height
                        write_in((i,j,lh),(i,j+1,lh),(i,j+1,hh),face_vector_xn) 
                        write_in((i,j,lh),(i,j+1,hh),(i,j,hh),face_vector_xn) 
                    #to compare with left
                if i != (m-1):
                    if data[i,j] > data[i+1,j]:
                        hh = data[i,j]
                        lh = data[i+1,j]
                        write_in((i+1,j+1,lh),(i+1,j,lh),(i+1,j,hh),face_vector_xp) 
                        write_in((i+1,j+1,lh),(i+1,j,hh),(i+1,j+1,hh),face_vector_xp)                     
                    # to compare with left
                if (j -1) >= 0:
                    if data[i,j] > data[i,j-1]:
                        hh = data[i,j]
                        lh = data[i,j-1]
                        write_in((i+1,j,lh),(i,j,lh),(i,j,hh),face_vector_yp) 
                        write_in((i+1,j,lh),(i,j,hh),(i+1,j,hh),face_vector_yp)                
                    # to compare with up
                if j != (n-1):
                    if data[i,j] > data[i,j+1]:
                        hh = data[i,j]
                        lh = data[i,j+1]
                        write_in((i,j+1,lh),(i+1,j+1,lh),(i+1,j+1,hh),face_vector_yn) 
                        write_in((i,j+1,lh),(i+1,j+1,hh),(i,j+1,hh),face_vector_yn)                    
                    # to compare with down

def build_roof(data):    
    m,n = shape(data)
    for i in range(m):
        for j in range(n):
            if data[i,j]:
                h = data[i,j]
                face_vector = (0,0,1)
                write_in((i,j,h),(i+1,j,h),(i,j+1,h),face_vector)
                write_in((i,j+1,h),(i+1,j,h),(i+1,j+1,h),face_vector)

def image2model(filename,gradient=10,width=100,height=10):
    data = loadDataSet(filename)
    m,n = shape(data)
    s = round((max(m,n)/width),1) 
    #width & height is the size of real model printed, so we need to know how much larger the model is.
    #grident is used to gredigest the pixel.
    height = height * s
    data = normalize(data,gradient,s)
        
    initial_wall(data,s,height)
    build_inwall(data,height)
    build_floor(data)
    build_prop(data)    
    build_roof(data)
    
    modellist.append('endsolid OpenSCAD_Model')
    
    name = filename.strip().split('.')[0]
    with open('%s.txt' % name,'w') as f:
        for line in modellist:
            f.write(line+'\n')
    print('The image %s has been tranlated to a 3D model' % name)

image2model('moon_test.jpg')        