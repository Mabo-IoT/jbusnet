## A jbusnet lib 
A simple jbusnet lib to parse jbusnet protocol

## Usage
```
jbusclient = Client(host="127.0.0.1", port=8001)
print(jbusclient.connect())
res = jbusclient.read_holding_registers(unit=0x01, address=0x00, length=0x10)
print(res.registers)
```