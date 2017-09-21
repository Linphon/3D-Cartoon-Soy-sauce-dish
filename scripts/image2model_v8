#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import *
import PIL.Image as image
import numpy as np
modellist = ['solid OpenSCAD_Model']

#read the image, and convert the type of data into numpy.array.
def loadDataSet(filename):
    data = np.asarray(image.open(filename).convert('L'))
    return data

#connect the coordinate with spacebar in order to write into the model file. 
def vector2str(vector):
    return ' '.join([str(i) for i in vector]) 

#refering the format of 3D model, a facet is consisted of three xyz coordinate and a face vector.
#this function is used to write in the information.
def write_in(x1,x2,x3,faceVector):
    line = '  facet normal ' + vector2str(faceVector)
    modellist.append(line)
    modellist.append('    outer loop')
    for vector in (x1,x2,x3):
        line = ' '*6 + 'vertex ' + vector2str(vector)
        modellist.append(line)
    modellist.append('    endloop')
    modellist.append('  endfacet')

#to process the values of pixels with a range of 255 into a smaller height range.
def normalize(data,gradient,s):
    num_gradient = int(ceil(255/gradient))
    out_data = data.copy()
    for i in range(num_gradient):
        out_data[(data>(i*gradient))*(data<=((i+1)*gradient))] = i
    scale = round((gradient*s/25.5),1)
    out_data = out_data * scale
    return out_data

#to initialize the outside wall of the model, which is used to hold the soy sauce.
def initial_wall(data,thick,height):
    m,n = shape(data)    
    face_vector_xp,face_vector_xn = (1,0,0),(-1,0,0)
    face_vector_yp,face_vector_yn = (0,1,0),(0,-1,0)
    face_vector_zp,face_vector_zn = (0,0,1),(0,0,-1)    
    
    #this is the floor.
    write_in((-thick,n+thick,-thick),(m+thick,n+thick,-thick),(-thick,-thick,-thick),face_vector_zn)
    write_in((-thick,-thick,-thick),(m+thick,n+thick,-thick),(m+thick,-thick,-thick),face_vector_zn)
    
    #this isy&z facet.
    write_in((m+thick,-thick,-thick),(m+thick,n+thick,-thick),(m+thick,n+thick,height),face_vector_xp)
    write_in((m+thick,-thick,height),(m+thick,-thick,-thick),(m+thick,n+thick,height),face_vector_xp)
    write_in((-thick,-thick,height),(-thick,n+thick,height),(-thick,-thick,-thick),face_vector_xn)
    write_in((-thick,-thick,-thick),(-thick,n+thick,height),(-thick,n+thick,-thick),face_vector_xn)
    
    #this is x&z facet.
    write_in((-thick,n+thick,-thick),(m+thick,n+thick,height),(m+thick,n+thick,-thick),face_vector_yp)
    write_in((-thick,n+thick,-thick),(-thick,n+thick,height),(m+thick,n+thick,height),face_vector_yp)
    write_in((-thick,-thick,-thick),(m+thick,-thick,-thick),(m+thick,-thick,height),face_vector_yn)
    write_in((-thick,-thick,height),(-thick,-thick,-thick),(m+thick,-thick,height),face_vector_yn)
    
    #this is roofs of outside walls.
    write_in((-thick,-thick,height),(m+thick,0,height),(m+thick,-thick,height),face_vector_zp) 
    write_in((-thick,-thick,height),(-thick,0,height),(m+thick,0,height),face_vector_zp) 
    write_in((-thick,n,height),(m+thick,n+thick,height),(m+thick,n,height),face_vector_zp) 
    write_in((-thick,n,height),(-thick,n+thick,height),(m+thick,n+thick,height),face_vector_zp) 
    write_in((-thick,0,height),(0,n,height),(0,0,height),face_vector_zp) 
    write_in((-thick,0,height),(-thick,n,height),(0,n,height),face_vector_zp) 
    write_in((m,0,height),(m+thick,n,height),(m+thick,0,height),face_vector_zp) 
    write_in((m,0,height),(m,n,height),(m+thick,n,height),face_vector_zp) 
    
#to build inthicknesside walls of the model, according to velues of pixels beside the wall.
def build_inwall(data,h):
    m,n = shape(data)
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

#to build the pillars under the pixel.                
def build_pillar(data):
    m,n = shape(data)
    face_vector_xp,face_vector_xn = (1,0,0),(-1,0,0)
    face_vector_yp,face_vector_yn = (0,1,0),(0,-1,0)
    for i in range(m):
        for j in range(n):
            if data[i,j]:
                if (i-1) >= 0:
                    if data[i,j] > data[i-1,j]:#to compare with right pixel
                        hh = data[i,j] # high height
                        lh = data[i-1,j] # low height
                        write_in((i,j,lh),(i,j+1,lh),(i,j+1,hh),face_vector_xn) 
                        write_in((i,j,lh),(i,j+1,hh),(i,j,hh),face_vector_xn) 
                    
                if i != (m-1):
                    if data[i,j] > data[i+1,j]:#to compare with left pixel
                        hh = data[i,j]
                        lh = data[i+1,j]
                        write_in((i+1,j+1,lh),(i+1,j,lh),(i+1,j,hh),face_vector_xp) 
                        write_in((i+1,j+1,lh),(i+1,j,hh),(i+1,j+1,hh),face_vector_xp)                     
                    
                if (j -1) >= 0:
                    if data[i,j] > data[i,j-1]:#to compare with top pixel
                        hh = data[i,j]
                        lh = data[i,j-1]
                        write_in((i+1,j,lh),(i,j,lh),(i,j,hh),face_vector_yp) 
                        write_in((i+1,j,lh),(i,j,hh),(i+1,j,hh),face_vector_yp)                
                    
                if j != (n-1):
                    if data[i,j] > data[i,j+1]:#to compare with below pixel
                        hh = data[i,j]
                        lh = data[i,j+1]
                        write_in((i,j+1,lh),(i+1,j+1,lh),(i+1,j+1,hh),face_vector_yn) 
                        write_in((i,j+1,lh),(i+1,j+1,hh),(i,j+1,hh),face_vector_yn)                    
                    
#a supporting function for build_roof, to find out the end point of a facet.
def find_point(i,start_point,data):
    m,n = shape(data)
    end_point = start_point + 1
    if start_point == n-1:
        return end_point
    elif data[i,start_point] != data[i,end_point]:
        return end_point
    else:
        return find_point(i,end_point,data)

#according to the value of pixel, build roof with different height.        
def build_roof(data):    
    m,n = shape(data)
    face_vector = (0,0,1)
    for i in range(m):
        j = 0
        while (j < n):
                h = data[i,j]
                end_point = find_point(i,j,data)                
                if h != 0:
                    write_in((i,j,h),(i+1,j,h),(i,end_point,h),face_vector)
                    write_in((i,end_point,h),(i+1,j,h),(i+1,end_point,h),face_vector)
                else:
                    write_in((i,j,0),(i+1,j,0),(i,end_point,0),face_vector)
                    write_in((i,end_point,0),(i+1,j,0),(i+1,end_point,0),face_vector) 
                j = end_point

#main function to connect supporting functions above.
def image2model(filename,gradient=10,width=100,height=10):
    data = loadDataSet(filename)
    m,n = shape(data)
    scale = round((max(m,n)/width),1) 
    '''width & height is the size of real model printed, 
    so we need to know how much larger the model is in 3D model before printed.'''   
    data = normalize(data,gradient,scale)    
    height = height * scale #hthe height of the outside wall is real height*scale.
    thickness = 2 * scale #the thickness of the outside wall is 2mm.
    
    initial_wall(data,thickness,height)
    build_inwall(data,height)
    build_pillar(data)    
    build_roof(data)    
    modellist.append('endsolid OpenSCAD_Model')
    
    name = filename.strip().split('.')[0]
    with open('%s.txt' % name,'w') as f:
        for line in modellist:
            f.write(line+'\n')
    print('The image %s has been tranlated to a 3D model' % name)

image2model('moon_test.jpg')        
