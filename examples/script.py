import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jbusnet.client import Client


def main():
    # must run jbus simulator py first if just run for test
    jbusclient = Client(host="127.0.0.1", port=8001)
    print(jbusclient.connect())
    res = jbusclient.read_holding_registers(unit=0x01, address=0x00, length=0x10)
    print(res.registers)

if __name__ == '__main__':
    main()