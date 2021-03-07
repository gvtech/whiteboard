#!/usr/bin/env python

import json
import pickle
from random import sample
from os.path import exists

import numpy as np
from tensorflow.keras.models import load_model

img_size=20

grid=10

class ShapeGenerator(object):
    def __init__(self):
        self.shapeList=[
                {"shape":"rectangle","x":100,"y":100,"dx":200,"dy":100},
                {"shape":"rectangle","x":100,"y":100,"dx":100,"dy":200},
                {"shape":"triangle","x":100,"y":100,"dx":200,"dy":100},
                {"shape":"triangle","x":100,"y":100,"dx":100,"dy":100},
                {"shape":"elipse","x":100,"y":100,"dx":200,"dy":100},
                {"shape":"elipse","x":100,"y":100,"dx":50,"dy":50},
                {"shape":"elipse","x":100,"y":100,"dx":50,"dy":200},
                {"shape":"vline","x":100,"y":100,"dx":0,"dy":100},
                {"shape":"hline","x":100,"y":100,"dx":200,"dy":0},
                {"shape":"upline","x":100,"y":100,"dx":100,"dy":100},
                {"shape":"downline","x":100,"y":100,"dx":100,"dy":100},
                {"shape":"sigma","x":100,"y":100,"dx":80,"dy":100},
                {"shape":"leftbracket","x":100,"y":100,"dx":20,"dy":50},
                {"shape":"rightbracket","x":100,"y":100,"dx":20,"dy":50},
                {"shape":"uparrow","x":100,"y":100,"dx":20,"dy":20},
                {"shape":"downarrow","x":100,"y":100,"dx":20,"dy":20},
                {"shape":"leftarrow","x":100,"y":100,"dx":20,"dy":20},
                {"shape":"rightarrow","x":100,"y":100,"dx":20,"dy":20},
                {"shape":"integral","x":100,"y":100,"dx":20,"dy":50}
                ]
        self.correspondingShapes={
            ("hline","hline"):self.halign,
            ("vline","vline"):self.valign,
            ("hline","rightarrow"):self.vcenter,
            ("hline","leftarrow"):self.vcenter,
            ("vline","uparrow"):self.hcenter,
            ("vline","downarrow"):self.hcenter,
            ("vline","hline"):self.connect,
            ("vline","downline"):self.connect,
            ("hline","vline"):self.connect,
            ("hline","upline"):self.connect,
            ("rightarrow","rightarrow"):self.resize,
            ("leftarrow","leftarrow"):self.resize,
            ("leftbracket","rightbracket"):self.resize
        }
        self.model=None
        self.labelEncoder=None
        
    def load_model(self):
        if self.model is None:
            modelDir="model"
            if exists(modelDir):
                self.model=load_model(modelDir)
                self.labelEncoder=pickle.load(open(modelDir+"/assets/labelEncoder.pickle","rb"))

    def chooseshape(self):
        shape=sample(self.shapeList,1)[0]
        shape["color"]="black"
        print("choosen shape ",shape)
        return shape

    def train(self,shape,lpoints):
        with open("data/training.json","a") as trainingFile:
            jsonStr=json.dumps({"shape":shape,"points":lpoints})
            trainingFile.write(jsonStr+"\n")
        print(shape+" added to training")

    def normalize_points(self,lpoints):
        p=np.array(lpoints)
        p=p-p.min(axis=0)
        return p/(p.max()+0.01)

    def build_image(self,lpoints):
        points=self.normalize_points(lpoints)
        img=np.zeros((img_size,img_size))
        for y,x in np.rollaxis(points, 0):
            img[int(x*img_size),int(y*img_size)]=1.0
        return img.reshape(1,img_size,img_size,1)

    def valign(self,shape,prevShape):
        if abs(shape["y"]-prevShape["y"])<grid:
            shape["y"]=prevShape["y"] 
        if abs(shape["dy"]-prevShape["dy"])<grid:
            shape["dy"]=prevShape["dy"] 

    def halign(self,shape,prevShape):
        if abs(shape["x"]-prevShape["x"])<grid:
            shape["x"]=prevShape["x"] 
        if abs(shape["dx"]-prevShape["dx"])<grid:
            shape["dx"]=prevShape["dx"] 

    def hcenter(self,shape,prevShape):
        if abs(shape["x"]+shape["dx"]//2-prevShape["x"])<grid:
            shape["x"]=prevShape["x"]-shape["dx"]//2 

    def vcenter(self,shape,prevShape):
        if abs(shape["y"]+shape["dy"]//2-prevShape["y"])<grid:
            shape["y"]=prevShape["y"]-shape["dy"]//2 

    def resize(self,shape,prevShape):
        if abs(shape["y"]-prevShape["y"])<grid:
            shape["y"]=prevShape["y"] 
        if abs(shape["dy"]-prevShape["dy"])<grid:
            shape["dy"]=prevShape["dy"] 
        if abs(shape["dx"]-prevShape["dx"])<grid:
            shape["dx"]=prevShape["dx"] 

    def connect(self,shape,prevShape):
        if abs(shape["y"]-prevShape["y"])<grid:
            shape["y"]=prevShape["y"] 
        if abs(shape["x"]-prevShape["x"])<grid:
            shape["x"]=prevShape["x"] 
        if abs(shape["x"]-(prevShape["x"]+prevShape["dx"]))<grid:
            shape["x"]=prevShape["x"]+prevShape["dx"] 
        if abs(shape["y"]-(prevShape["y"]+prevShape["dy"]))<grid:
            shape["y"]=prevShape["y"]+prevShape["dy"] 

    def align_shape(self,shape,prevShape):
        couple=(prevShape["shape"],shape["shape"])
        if couple in self.correspondingShapes:
            self.correspondingShapes[couple](shape,prevShape)

    def guess_shape(self,lpoints,prevShapes):
        self.load_model()
        minx=min([x for x,_ in lpoints])
        miny=min([y for _,y in lpoints])
        maxx=max([x for x,_ in lpoints])
        maxy=max([y for _,y in lpoints])
        if self.model is not None:
            prediction=self.model.predict(self.build_image(lpoints))
            shapeform=self.labelEncoder.inverse_transform(prediction.argmax(axis=1))[0]
        else:
            shapeform="rectangle"
        shape={"shape":shapeform,"x":minx,"y":miny,"dx":maxx-minx,"dy":maxy-miny}
        if prevShapes!=[]:
            self.align_shape(shape,prevShapes[-1])
        return shape 

