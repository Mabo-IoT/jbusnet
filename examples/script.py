import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jbusnet.client import Client


def main():
    # must run jbus simulator py first if just run for test
    jbusclient = Client(host="192.168.134.162", port=7777)
    print(jbusclient.connect())
    while True:
        res = jbusclient.read_input_registers(unit=0x01, address=0xec13, length=0x10)
        print(res.registers)
        time.sleep(1)

if __name__ == '__main__':
    main()