# Jumpstarter Drivers

Jumpstarter uses Python modules called drivers to interact with the hardware interfaces connected to the Device Under Test (DUT).

Similar to the drivers used by your operating system, drivers in Jumpstarter enable the us to interact with hardware and provide abstractions that make that it easier to use.

Drivers in Jumpstarter consist of two components:

- A `Driver`, which implements the desired abstractions for a type of interface connected to the exporter machine. e.g. a TCP port.
- A `DriverClient`, which provides a user-friendly interface that can be used by clients to interact with the underlying `Driver` either locally or remotely over the network.