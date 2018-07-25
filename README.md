## A jbusnet lib 
A simple jbusnet lib to parse jbusnet protocol

## Usage
```
from jbusnet.client import Client

jbusclient = Client(host="127.0.0.1", port=8001)  # jbus host and port is required
print(jbusclient.connect())                # check if connected
res = jbusclient.read_holding_registers(unit=0x01, address=0x00, length=0x10)
print(res.registers)
```