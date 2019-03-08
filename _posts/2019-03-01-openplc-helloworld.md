---
layout: post
title: Hello World for OpenPLC and Modbus on Windows SoftPLC
date: 2019-03-01
---

My explortations into PLC runtimes has taken me to discover [OpenPLC](https://www.openplcproject.com/).
The goal of this post is to explain how I was able to depoy a "Hello World" project running on the
Windows SoftPLC and connected to a Modbus client.

To get started, I followed the [Creating You First Project](https://www.openplcproject.com/reference-your-first-project)
and deployed to the SoftPLC running on my machine. However, when I created the project, I used
a different mapping for the IO so that I would be able to control them from Python.

| Name  | Location  | Alternative Location |
|-------|-----------|----------------------|
| `PB1` | `%IX0.0`  | `%QX0.1`             |
| `PB2` | `%IX0.1`  | `%QX0.2`             |
| `LED` | `%IX0.0`  | `%QX0.0` (unchanged) |

As above, this maps all items to coils that support both read and write.

The next step is to connect to it via Modbus. To do this, I write a simple Modbus client using
[pymodbus](https://github.com/riptideio/pymodbus).

```
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time

client = ModbusClient('localhost', port=502)

unit=0x01

# Get the initial state
rr = client.read_coils(0, 1, unit=unit)
print("Initial LED output: " + str(rr.getBit(0)))
time.sleep(1)

client.write_coil(1, True, unit=unit)
print("Pressed PB1 - turn on LED")
time.sleep(1)

client.write_coil(1, False, unit=unit)
print("Unpressed PB1")
time.sleep(1)

rr = client.read_coils(0, 1, unit=unit)
print("LED output after pressing PB1: " + str(rr.getBit(0)))
time.sleep(1)

client.write_coil(2, True, unit=unit)
print("Pressed PB2 - reset")
time.sleep(1)

client.write_coil(2, False, unit=unit)
print("Unpressed PB2")
time.sleep(1)

rr = client.read_coils(0, 1, unit=unit)
print("LED output after pressing PB2 (reset): " + str(rr.getBit(0)))
time.sleep(1)

client.close()
```

Running that with Python produces the expected output:

```
python .\mobus-client.py
Initial LED output: False
Pressed PB1 - turn on LED
Unpressed PB1
LED output after pressing PB1: True
Pressed PB2 - reset
Unpressed PB2
LED output after pressing PB2 (reset): False
```

