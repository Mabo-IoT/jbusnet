import logging
import time

from abc import ABCMeta, abstractmethod
 
from jbusnet.utils import  convert_int_bytes, connect_bytes

_logger = logging.getLogger(__name__)



class PDU:
    def __init__(self, function_code, function_specific_data):
        """
        all param is bytes
        """
        self.function_code = function_code
        self.function_specific_data = function_specific_data
    
    @classmethod
    def make_request_pdu(cls, function_code, address, length):
        """
        make request PDU by request
        """
        function_specific_data = connect_bytes(convert_int_bytes(address, 2), convert_int_bytes(length, 2))
        function_code  = convert_int_bytes(function_code, 1)

        return cls(function_code, function_specific_data)
        
    @classmethod
    def make_response_pdu(cls, bytes):
        """
        make response PDU by response bytes
        """
        pass
    
    @property
    def bytes(self):
        """
        convert self to bytes
        """
        bytes_data = connect_bytes(self.function_code, self.function_specific_data)

        return bytes_data
    
    # def __call__(self):
    #     return self.bytes
        