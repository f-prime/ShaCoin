import socket
import json
import config
import random

def send(cmd, out=False, god=False):
    if god:
        nodes = config.brokers
    else:
        nodes = config.nodes.find("nodes", {"relay":1})
        random.shuffle(nodes)
    if not nodes:
        nodes = config.brokers
    for x in nodes:
        s = socket.socket()
        try:
            s.settimeout(30)
            s.connect((x['ip'], x['port']))
        except:
            s.close()
            continue
        else:
            s.send(json.dumps({"cmd":"get_version"}))
            try:
                data = s.recv(1024)
            except:
                s.close()
                continue
            if data == config.version:
                s.close()
                s = socket.socket()
                try:
                    s.settimeout(30)
                    s.connect((x['ip'], x['port']))
                except:
                    s.close()
                    continue
                else:
                    s.send(json.dumps(cmd))
                    out = ""
                    cont = False
                    while True:
                        try:
                            data = s.recv(1024)
                        except:
                            cont = True
                            break
                        if not data:
                            break
                        out = out + data
                    s.close()
                    if cont:
                        continue
                    if out:
                        return out
            else:
                s.close()

