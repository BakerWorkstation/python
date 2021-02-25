'''
@Author: your name
@Date: 2020-06-15 09:37:50
@LastEditTime: 2020-06-15 09:48:36
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/websocket/websocketClient_1.py
'''
#!/usr/bin/env python

import os
import ssl
import pathlib
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(10):
            time.sleep(0.1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    localhost_pem = pathlib.Path(__file__).with_name("server.pem")
    ssl_context.load_verify_locations(localhost_pem)
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://10.255.175.109:4500/api/v1/device/ptd/remote_access/test_1",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    print(1)
    #ws.run_forever(sslopt={"cert_regs": ssl_context})
    ws.run_forever(sslopt={"cert_regs": ssl.CERT_NONE, "check_hostname": False})
