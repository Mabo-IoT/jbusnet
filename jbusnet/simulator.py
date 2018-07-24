import logging
import random
import sys


from socketserver import BaseRequestHandler, ThreadingTCPServer
from utils import connect_bytes, calculate_crc

class JbusHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from {}'.format(self.client_address))
        
        while True:
            msg = self.request.recv(1024)
            
            if not msg:
                break
            
            unit = msg[0:1]
            function_code = msg[1:2]
            length = msg[4:6]
            
            bytes_data = make_response_bytes(unit, function_code, length)

            self.request.send(bytes_data)
    


def make_response_bytes(unit, function_code, length):
    """
    make jbus response bytes data
    """
    len = int(0)
    print(length)
    length = len.from_bytes(length, 'big') 
    
    length = length * 2

    contents = generate_contents(length)

    length_bytes = length.to_bytes(1, 'big')

    bytes_data = connect_bytes(unit, function_code, length_bytes, contents)
    
    crc = calculate_crc(bytes_data)

    response_bytes_data = connect_bytes(bytes_data, crc)

    return response_bytes_data



def generate_contents(length):
    """
    generate random contents bytes
    """
    print(length)
    contents = random.sample(range(100), length)
    bytes_data = memoryview(bytearray(contents)).tobytes()

    return bytes_data

if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 8001), JbusHandler)
    serv.serve_forever()