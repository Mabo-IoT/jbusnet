import logging
import time
import struct

from abc import ABCMeta, abstractmethod
from jbusnet.utils import calculate_crc

_logger = logging.getLogger(__name__)


class ResponseBase(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def make_response(self, bytes):
        pass

    @property
    @abstractmethod
    def registers(self):
        pass

    @property
    @abstractmethod
    def unit_id(self):
        pass
    
    @property
    @abstractmethod
    def function_code(self):
        pass
    


class Response(ResponseBase):
    def __init__(self, unit, function_code, length, contents):
        """
        Attention! all this data is bytes
        """
        self.unit = unit
        self.function_id = function_code
        self.length = length
        self.contents = contents
    
    @classmethod
    def make_response(cls, bytes_data):
        
        print("response is {}".format(bytes_data))
        unit = bytes_data[0:1]
        function_code = bytes_data[1:2]
        length = bytes_data[2:3]
        contents = bytes_data[3:-2]
        crc = bytes_data[-2:]
        function_specific_data = bytes_data[:-2]        

        if cls.check_crc(function_specific_data, crc):
            return cls(unit, function_code, length, contents)
        
        else:
            _logger.error("CRC  {} is unright".format(crc))
            raise Exception("CRC is unright please check recv data")

    @staticmethod
    def check_crc(function_specific_data, crc):
        """
        check crc if right
        """
        crc_cal = calculate_crc(function_specific_data)
        
        if crc == crc_cal:
            return True
        else:
            return False
    
    @property
    def function_code(self):
        data = int(0)
        return data.from_bytes(self.function_id, 'big')
    
    @property
    def unit_id(self):
        data = int(0)
        return data.from_bytes(self.unit, 'big')
    
    @property
    def registers(self):
        """
        return a list of contents
        """
        data = int(0)
        # length = data.from_bytes(self.length, 'big')
        length = len(self.contents)
        print("recv data length is {}".format(length))
        format = '!%dH'% (length/2)
        # print(len(self.contents))
        registers_data =  struct.unpack(format, self.contents)

        return list(registers_data)





        
        
    