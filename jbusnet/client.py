import logging
import time

from abc import ABCMeta, abstractmethod

from jbusnet.transition import Transition
from jbusnet.request import Request


_logger = logging.getLogger(__name__)


class BaseClient(metaclass=ABCMeta):
    @abstractmethod
    def read_holding_registers():
        pass
    

class Client(BaseClient):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.transition =  Transition(host=host, port=port)
    
    def connect(self):
        """
        init a socket client
        """
        return self.transition.connect()
    
    def read_holding_registers(self, unit, address, length):
        """
        read holding registers from jbus slave
        """
        # generate jbus request 
        request = Request(function_code=3, unit=unit, address=address, length=length)
        
        _logger.debug("Request is {}".format(request.bytes))

        # generate jbus response
        response = self.transition.execute(request)
        return response




