import logging
import time

from abc import ABCMeta, abstractmethod
from jbusnet.pdu import PDU

from jbusnet.utils import connect_bytes, convert_int_bytes, calculate_crc

_logger = logging.getLogger(__name__)


class RequstBase(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def bytes():
        pass


class Request(RequstBase):
    def __init__(self, unit, function_code, address, length):
        self.unit = unit
        self.pdu = PDU.make_request_pdu(function_code, address, length)
        self.CRC = calculate_crc(connect_bytes(convert_int_bytes(self.unit, 1), self.pdu.bytes))
    
    @property
    def bytes(self):
        """
        convert request to bytes
        """
        bytes_data = connect_bytes(convert_int_bytes(self.unit, 1), self.pdu.bytes, self.CRC)
        print(bytes_data)
        
        return bytes_data

        
        