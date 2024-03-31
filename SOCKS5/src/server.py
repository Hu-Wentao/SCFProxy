"""
在云函数中创建socks5服务
https://www.wangan.com/p/7fy7f36b5e17cc1e
"""
import json
import os
import select
import socket

# 安装client的服务器所配置的ip与端口
bridge_ip = os.getenv('BRIDGE_IP')
bridge_port = os.getenv("BRIDGE_PORT")


def main_handler(event, context):
    data = json.loads(event["body"])
    out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    out.connect((data["host"], data["port"]))

    bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bridge.connect((bridge_ip, int(bridge_port)))
    bridge.send(data["uid"].encode("ascii"))

    while True:
        readable, _, _ = select.select([out, bridge], [], [])
        if out in readable:
            data = out.recv(4096)
            bridge.send(data)
        if bridge in readable:
            data = bridge.recv(4096)
            out.send(data)
