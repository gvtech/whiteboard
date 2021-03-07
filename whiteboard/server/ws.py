#!/usr/bin/env python

import json
import asyncio
from collections import defaultdict
from server.shape import ShapeGenerator

class ShapeServer(object):
    def __init__(self):
        self.users = {}
        self.drawing=defaultdict(list)
        self.shapes=defaultdict(list)
        self.shapeGenerator=ShapeGenerator()

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
        if uid in self.shapes:
            del self.shapes[uid]

    async def send_user(self,uid,msg):
        try:
            print(f"sending to: {uid}  info {msg}")
            await self.users[uid].send_json(msg)
        except Exception as e:
            print("connection closed ",uid,e)
            self.remove_user(uid)

    async def send_all_users(self,msg,omitUser=None):
        await asyncio.gather(*[self.send_user(uid,msg)         
                            for uid in list(self.users.keys()) if uid!=omitUser])

    async def process_message(self,msg,websocket):
        if "uid" in msg:
            curuid=msg["uid"]
            await self.send_all_users(msg,omitUser=curuid)
            if msg["action"]=="start":
                self.drawing[curuid]=[]
            self.drawing[curuid].append((msg["x"],msg["y"]))
            if msg["action"]=="draw" and len(self.drawing[curuid])>5:
                shape=self.shapeGenerator.guess_shape(self.drawing[curuid],self.shapes[curuid])
                shape["uid"]=curuid
                shape["color"]=msg["color"]
                self.shapes[curuid].append(shape)
                await self.send_all_users(shape)

            if msg["action"]=="train":
                self.shapeGenerator.train(msg["shape"],self.drawing[curuid])
            
        else:
            curuid=self.add_user(websocket)
            print("new connection made %d"%curuid)
            await websocket.send_json({"setuid":curuid})

