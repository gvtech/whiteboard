#!/usr/bin/env python

import json
import pickle
import asyncio
import aiohttp 
from aiohttp import web

from server.ws import ShapeServer

routes = web.RouteTableDef()
shapeServer=ShapeServer()

@routes.get('/')
async def root(request):
    raise web.HTTPFound('/views/whiteboard.html')

@routes.get('/index.html')
async def index(request):
    raise web.HTTPFound('/views/whiteboard.html')

@routes.get('/chooseshape')
async def chooseshape(request):
    shape=shapeServer.shapeGenerator.chooseshape()
    await shapeServer.send_all_users(shape)
    return web.json_response(shape)

@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await shapeServer.process_message(json.loads(msg.data),ws   )
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')

app = web.Application()
app.add_routes(routes)
for subpath in ("views","images","css","js"):
    app.router.add_static("/"+subpath,path="static/"+subpath,name=subpath)

web.run_app(app)

