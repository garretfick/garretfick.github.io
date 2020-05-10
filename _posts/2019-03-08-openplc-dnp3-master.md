---
layout: post
title: OpenPLC DNP3 Master Mappings
date: 2019-03-08
---

OpenPLC supports DNP3 on the SoftPLC platform (except for Windows). This post describes how I was
able to interact with the DNP3 slave (outstation) running on Linux SoftPLC. This post follows the
same work I did with Modbus, but using DNP3.

The HelloWorld project is designed for reading inputs from physical hardware, but we will toggle
inputs over DNP3, so we need to change the location mapping to points that we can write to. This
is the same as what we did with Modbus.

Update the design as follows:

| Name  | Location | DNP3 Group | DNP3 Variation | DNP3 Index |
|-------|----------|------------|----------------|------------|
| `PB1` | `%QX0.1` | 12         | 2              | 1          |
| `PB2` | `%QX0.2` | 12         | 2              | 2          |
| `LED` | `%QX0.0` | 10         | 2              | 0          |

Upload the program as per normal using the web interface. By default, Modbus is enabled and DNP3 is disabled. In the web interface:

1. Go to *Settings*
1. Uncheck *Enable Modbus Server* and check *Enable DNP3 Server*, then select *Save Changes*.

The next step is to connect to it via DNP3. OpenPLC is always the outstation, which means you need to connect to it as
the master. You can implement this in a number of languages, and for this demonstration, I'm using Python and pydnp3.

As far as I know, it is not available via PIP, so you need to get the code and set it up yourself (and your already on Linux already because that's the supported platform for DNP3 and OpenPLC). Get the code from https://github.com/ChargePoint/pydnp3 and follow the instructions in the readme to setup your system.

Finally, we can connect to the oustation via DNP3 to control the device.

```python
from pydnp3 import opendnp3, openpal, asiopal, asiodnp3
import time

# In a production application, you need to handle the asynchronous
# API of OpenDNP3. I'm forgoing that for now to demonstrate the
# key capabililties that are needed.
SLEEP_SECONDS = 5

# Create the manager for DNP3. This is always the first thing you
# need to do for OpenDNP3.
log_handler = asiodnp3.ConsoleLogger().Create()
manager = asiodnp3.DNP3Manager(1, log_handler)

# Next we need a channel. We are going to communicate over TCP
# (as opposed to TLS), so create a TCP channel. I'm also assuming
# that the Soft PLC is running on the same machine with the 
# standard DNP3 port.
retry = asiopal.ChannelRetry().Default()
listener = asiodnp3.PrintingChannelListener().Create()
channel = manager.AddTCPClient('client', opendnp3.levels.NOTHING, retry, '127.0.0.1', '0.0.0.0', 20000, listener)

# OpenDNP3 is very much object-oriented. In order for use to read the actual
# binary values, we must implement the visitor. This visitor just stores all
# of the values in this instance so we can read it later.
class VisitorIndexedBinaryOutputStatus(opendnp3.IVisitorIndexedBinaryOutputStatus):
    def __init__(self):
        super(VisitorIndexedBinaryOutputStatus, self).__init__()
        self.index_and_value = []

    def OnValue(self, indexed_instance):
        self.index_and_value.append((indexed_instance.index, indexed_instance.value.value))

# The sequence of events handler - this receives measurment
# data from the master and prints it to the console. We need
# a custom implementation because the default printing one is
# not so useful
class SOEHandler(opendnp3.ISOEHandler):
    def __init__(self):
        super(SOEHandler, self).__init__()

    def Process(self, info, values):
        if (values.Count() == 4 and type(values) == opendnp3.ICollectionIndexedBinaryOutputStatus):
            class BOSVisitor(opendnp3.IVisitorIndexedBinaryOutputStatus):
                def __init__(self):
                    super(BOSVisitor, self).__init__()
                def OnValue(self, indexed_instance):
                    print(indexed_instance.index, indexed_instance.value.value)
            values.Foreach(BOSVisitor())

    def Start(self):
        # This is implementing an interface, so this function
        # must be declared.
        pass

    def End(self):
        # This is implementing an interface, so this function
        # must be declared.
        pass

soe_handler = SOEHandler()

# OpenPLC is the outstation and we are the master. So, we want to add
# to the TCP channel that we are the master. After this, we are configured
# to communicate over DNP3.
master_application = asiodnp3.DefaultMasterApplication().Create()
stack_config = asiodnp3.MasterStackConfig()
stack_config.master.responseTimeout = openpal.TimeDuration().Seconds(2)
stack_config.link.RemoteAddr = 10
master = channel.AddMaster('master', soe_handler, master_application, stack_config)
master.Enable()

time.sleep(SLEEP_SECONDS)

# Read the initial binary outputs on the device (the outstation)
# There are a few ways we can achieve  this - such as scanning by
# class or range. Either one of these will read the exposed points.
# The difference here is in how much data we receive. The logging
# of what we read is handled by the SOE handler we setup above. There
# is no direct way to make this a blocking operation, so we just sleep
# for a while once we have made the request to read.
#master.ScanClasses(opendnp3.ClassField(opendnp3.ClassField.CLASS_0))
print('\nReading initial status')
NUMBER_OF_OUTPUTS = 3
group_variation = opendnp3.GroupVariationID(10, 2)
master.ScanRange(group_variation, 0, NUMBER_OF_OUTPUTS)
time.sleep(SLEEP_SECONDS)

# Next, we want to toggle the switch PB1 to turn on the LED. That swith
# is at binary input index 0.
print('\nToggling the switch to turn on the LED')
command_callback = asiodnp3.PrintingCommandCallback.Get()
command_set = opendnp3.CommandSet([
    opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 1),
])
master.DirectOperate(command_set, command_callback)
time.sleep(SLEEP_SECONDS)

print('\nToggling the switch to turn on the LED - latch off')
command_callback = asiodnp3.PrintingCommandCallback.Get()
command_set = opendnp3.CommandSet([
    opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF), 1)
])
master.DirectOperate(command_set, command_callback)
time.sleep(SLEEP_SECONDS)

print('\nReading status after turning on the LED')
master.ScanRange(group_variation, 0, NUMBER_OF_OUTPUTS)
time.sleep(SLEEP_SECONDS)

# Next, we want to toggle the switch PB2 to turn off the LED
print('\nToggling the swtich to turn off the LED')
command_callback = asiodnp3.PrintingCommandCallback.Get()
command_set = opendnp3.CommandSet([
    opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 2)
])
master.DirectOperate(command_set, command_callback)
time.sleep(SLEEP_SECONDS)

print('\nToggling the switch to turn on the LED - latch off')
command_callback = asiodnp3.PrintingCommandCallback.Get()
command_set = opendnp3.CommandSet([
    opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF), 2)
])
master.DirectOperate(command_set, command_callback)
time.sleep(SLEEP_SECONDS)

print('\nReading status after turning on the LED back off')
master.ScanRange(group_variation, 0, NUMBER_OF_OUTPUTS)
time.sleep(SLEEP_SECONDS)

# When terminating, it is necessary to set these to None so that
# it releases the shared pointer. Otherwise, python will not
# terminate (and even worse, the normal Ctrl+C won't help).
master.Disable()
master = None
channel.Shutdown()
channel = None
manager.Shutdown()

```

My my machine, this produces the following:

```
ms(1552335400119) INFO    manager - Starting thread (0)
channel state change: OPENING
channel state change: OPEN

Reading initial status
(0, False)
(1, False)
(2, False)

Toggling the switch to turn on the LED
Received command result w/ summary: SUCCESS
Header: 0 Index: 1 State: SUCCESS Status: SUCCESS
Toggling the switch to turn on the LED - latch off
Received command result w/ summary: SUCCESS
Header: 0 Index: 1 State: SUCCESS Status: SUCCESS
Reading status after turning on the LED
(0, True)
(1, False)
(2, False)

Toggling the swtich to turn off the LED
Received command result w/ summary: SUCCESS
Header: 0 Index: 2 State: SUCCESS Status: SUCCESS
Toggling the switch to turn on the LED - latch off
Received command result w/ summary: SUCCESS
Header: 0 Index: 2 State: SUCCESS Status: SUCCESS
Reading status after turning on the LED back off
(0, False)
(1, False)
(2, False)
channel state change: CLOSED
channel state change: SHUTDOWN
ms(1552335440148) INFO    manager - Exiting thread (0)
```
