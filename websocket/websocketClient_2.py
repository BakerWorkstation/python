'''
@Author: your name
@Date: 2020-06-15 09:38:08
@LastEditTime: 2020-06-15 09:55:04
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/websocket/websocketClient_2.py
'''
#!/usr/bin/env python

import ssl
import time
import asyncio
import pathlib
import websockets

#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
localhost_pem = pathlib.Path(__file__).with_name("server.pem")
ssl_context.load_verify_locations(localhost_pem)

async def hello():
    #uri = "wss://10.255.175.109:4500/api/v1/device/ptd/remote_access/test_1"
    uri = "wss://10.255.175.109:4500/api/internal/remote_access/device/ptd/data/test_1/123123"
    async with websockets.connect(
        uri, ssl=ssl_context
    ) as websocket:
        print("open")
        name = input("What's your name? ")
        print(f"> {name}")
        await websocket.send(name)
        greeting = await websocket.recv()
        print(greeting)
        
        print("close")
        time.sleep(100)
            

asyncio.get_event_loop().run_until_complete(hello())
print(dir(asyncio.get_event_loop()))
