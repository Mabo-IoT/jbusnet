import logging
import time

from abc import ABCMeta, abstractmethod

__logger = logging.getLogger(__name__)

byte2int = lambda b: b


def convert_int_bytes(data, length):
    """
    convert int to bytes
    data: int value
    length: bytes number
    """
    bytes_data = data.to_bytes(length, 'big')
    
    return bytes_data 


def connect_bytes(bytes_data, *args):
    """
    connect bytes 1,2...to a bytes
    """
    # print("{} is connected ".format(bytes_data))
    bytes_list = list(bytes_data)

    for bytes_d in args:
        bytes_data = bytes_data + bytes_d
    
    return bytes(bytes_data)
    
    
def __generate_crc16_table():
    """ Generates a crc16 lookup table

    .. note:: This will only be generated once
    """
    result = []
    for byte in range(256):
        crc = 0x0000
        for _ in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xa001
            else: crc >>= 1
            byte >>= 1
        result.append(crc)
    return result

__crc16_table = __generate_crc16_table()

def calculate_crc(bytes_data):
    """ Computes a crc16 on the passed in string. For modbus,
    this is only used on the binary serial protocols (in this
    case RTU).

    The difference between modbus's crc16 and a normal crc16
    is that modbus starts the crc value out at 0xffff.

    :param data: The data to create a crc16 of
    :returns: The calculated CRC
    """

    crc = 0xffff

    for a in bytes_data:
        idx = __crc16_table[(crc ^ byte2int(a)) & 0xff]
        crc = ((crc >> 8) & 0xff) ^ idx
    swapped = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)

    crc_bytes = swapped.to_bytes(2, 'big') # 2 bytes and format as bid byteorder

    return crc_bytes


