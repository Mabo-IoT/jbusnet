import logging
from socket import socket, AF_INET, SOCK_STREAM
from abc import ABCMeta, abstractmethod

from jbusnet.response import Response

_logger = logging.getLogger(__name__)


class TransitionBase(metaclass=ABCMeta):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def execute(self, request):
        pass


class Transition(TransitionBase):
    """
    send request and recv data and make data to a response
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # init sockect  client 

        self._init()
        
    
    def _init(self):
        """
        init socket client
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        
        try:
            self.socket.connect((self.host, self.port))
        
        except Exception as e:
            _logger.error(e)

    def connect(self):
        """
        test self client if connect
        """
        if self.socket.getsockname():
            return True
        
        else: 
            return False
    
    def execute(self, request):
        """
        send request data to slave and wait for response
        """
        send_data = request.bytes
        self.socket.send(send_data)
        
        recv_data = self.socket.recv(1024)
        
        response = Response.make_response(recv_data)
        return response
