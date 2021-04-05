#!/usr/bin/env python

import json
import pickle
import asyncio
import aiohttp 
from aiohttp import web
import argparse

from server.ws import ShapeServer

parser = argparse.ArgumentParser()
parser.add_argument("--boarddir", type=str,help="Board storing dir",default="./boards")
args = parser.parse_args()

routes = web.RouteTableDef()
shapeServer=ShapeServer(rootdir=args.boarddir)

@routes.get('/')
async def root(request):
    raise web.HTTPFound('/views/whiteboard.html')

@routes.get('/index.html')
async def index(request):
    raise web.HTTPFound('/views/whiteboard.html')

@routes.get('/chooseshape')
async def chooseshape(request):
    shape=shapeServer.shapeGenerator.chooseshape()
#    await shapeServer.send_all_users(shape)
    return web.json_response(shape)

@routes.get('/newboard')
async def newboard(request):
    board= await shapeServer.new_board()
    return web.json_response({"boardId":board.boardId})

@routes.get('/openboard/{boardid}')
async def boardid(request):
    boardid=request.match_info["boardid"]
    board= await shapeServer.open_board(boardid)
    return web.json_response(board.shapeList)

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

loop=asyncio.get_event_loop()

app = web.Application(loop=loop)
app.add_routes(routes)
for subpath in ("views","images","css","js"):
    app.router.add_static("/"+subpath,path="static/"+subpath,name=subpath)

loop.call_later(60,shapeServer.backup_boards,loop)
web.run_app(app)

