#!/usr/bin/env python

import json
import asyncio
from collections import defaultdict
from server.shape import ShapeGenerator
from server.board import BoardStore

class ShapeServer(object):
    def __init__(self,rootdir="./boards"):
        self.users = {}
        self.drawing=defaultdict(list)
        self.userboard=dict()
        self.boardstore=BoardStore(rootdir=rootdir)
        self.shapeGenerator=ShapeGenerator()

    async def new_board(self):
        return self.boardstore.newBoard()

    async def open_board(self,boardId):
        return self.boardstore.getBoard(boardId)

    def backup_boards(self,loop):
        print("saving boards")
        self.boardstore.backup()
        loop.call_later(60,self.backup_boards,loop)

    def add_user(self,websocket):
        uid=0
        while uid in self.users:
            uid+=1
        self.users[uid]=websocket
        return uid

    def remove_user(self,uid):
        print("removing user",uid)
        if uid in self.users:
            del self.users[uid]
        if uid in self.drawing:
            del self.drawing[uid]
        if uid in self.userboard:
            del self.userboard[uid]

    async def send_user(self,uid,msg):
        try:
            print(f"sending to: {uid}  info {msg}")
            await self.users[uid].send_json(msg)
        except Exception as e:
            print("connection closed ",uid,e)
            self.remove_user(uid)

    async def send_all_board_users(self,boardId,msg,omitUser=None):
        boardusers=[uid for uid in self.users.keys() if uid!=omitUser and self.userboard.get(uid,None).boardId==boardId]
        await asyncio.gather(*[self.send_user(uid,msg) for uid in boardusers])

    async def process_message(self,msg,websocket):
#        print(msg)
        if "uid" in msg:
            curuid=msg["uid"]
            if msg["action"]=="openboard":
                self.userboard[curuid]=self.boardstore.getBoard(msg["boardid"])
            else:
                curboard=self.userboard[curuid]
                if msg["action"]=="start":
                    self.drawing[curuid]=[]
                    self.drawing[curuid].append((msg["x"],msg["y"]))
                    await self.send_all_board_users(curboard.boardId,msg,omitUser=curuid)

                elif msg["action"]=="move":
                    self.drawing[curuid].append((msg["x"],msg["y"]))
                    await self.send_all_board_users(curboard.boardId,msg,omitUser=curuid)

                elif msg["action"]=="draw" and len(self.drawing[curuid])>5:
                    shape=self.shapeGenerator.guess_shape(self.drawing[curuid],curboard.shapeList)
                    shape["uid"]=curuid
                    shape["color"]=msg["color"]
                    curboard.add(shape)
                    await self.send_all_board_users(curboard.boardId,shape)

                elif msg["action"]=="train":
                    self.shapeGenerator.train(msg["shape"],self.drawing[curuid])
            
        else:
            curuid=self.add_user(websocket)
            print("new connection made %d"%curuid)
            await websocket.send_json({"setuid":curuid})

