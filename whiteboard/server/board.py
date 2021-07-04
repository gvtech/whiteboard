#!/usr/bin/env python

import json
from uuid import uuid1
from os import makedirs
from os.path import exists
from time import time

class Board(object):
    def __init__(self,fromId=None,rootdir="./boards"):
        self.rootdir=rootdir
        if fromId is None:
            self.boardId=uuid1().hex
            self.shapeList=[]
        else:
            self.load(fromId)
        self.timestamp=time()
        self.lastsave=self.timestamp

    def __iter__(self):
        for shape in self.shapeList:
            yield shape

    def load(self,fromId):
        self.boardId=fromId
        dir=self.rootdir+"/"+self.boardId[:2]
        filename=f"{dir}/{self.boardId[2:]}.json"
        if exists(filename):
            self.shapeList=json.load(open(filename))
        else:
            self.shapeList=[]

    def save(self):
        if self.timestamp>self.lastsave:
            dir=self.rootdir+"/"+self.boardId[:2]
            makedirs(dir,exist_ok=True)
            filename=f"{dir}/{self.boardId[2:]}.json"
            json.dump(self.shapeList,open(filename,"w"))
            self.lastsave=self.timestamp

    def add(self,shape):
        self.shapeList.append(shape)
        self.timestamp=time()
    
    def can_undo(self):
        return len(self.shapeList)>1

    def undo(self):
        self.timestamp=time()
        return self.shapeList.pop(-1)

class BoardStore(object):
    def __init__(self,rootdir="./boards"):
        self.rootdir=rootdir
        self.boards=dict()

    def getBoard(self,boardId):
        if boardId in self.boards:
            return self.boards[boardId]
        else:
            board=Board(fromId=boardId,rootdir=self.rootdir)
            self.boards[board.boardId]=board
            return board

    def newBoard(self):
        board=Board()
        self.boards[board.boardId]=board
        return board

    def backup(self):
        lclean=[]
        for boardId,board in self.boards.items():
            board.save()
            if (time()-board.timestamp) > 300:
                lclean.append(boardId)
        for boardId in lclean:
            del self.boards[boardId]



        