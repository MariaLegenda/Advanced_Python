import yaml
import json
import socket
import zlib
import threading
from datetime import datetime
from argparse import ArgumentParser

WRITE_MODE = 'write'

READ_MODE = 'read'

def read(sock, buffersize):
    while True:
        response = sock.recv(buffersize)
        bytes_response = zlib.decompress(response)
        print(bytes_response.decode())

def make_request(action, data):
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
    }

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='Sets config file path'
)

parser.add_argument(
    '-m', '--mode', type=str, default=WRITE_MODE,
    help='Sets client mode'
)

args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)

host, port = config.get('host'), config.get('port')

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client was started')

    read_thread = threading.Tread(
        target=read, args=(sock, config.get('buffersize'))
    )
        read_thread.start()



    while True:
        args.mode == WRITE_MODE:
        action = input('Enter action: ')
        data = input('Enter data: ')

        request = make_request(action, data)
        str_request = json.dumps(request)
        bytes_request = zlib.compress(str_request.encode())

        sock.send(bytes_request)
        print(f'Client send data { data }')

except KeyboardInterrupt:
    print('client shutdown.')



