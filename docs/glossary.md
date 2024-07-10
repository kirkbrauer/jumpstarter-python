# Jumpstarter glossary

## Acronyms

* `DUT`: Device Under Test - the device that is being tested using Jumpstarter.

## Entities

* `Exporter`: A Linux service that exports the interfaces to the DUTs.
  An exporter connects directy to a Jumpstarter server or directly to a client.

* `Device`: A DUT that is exposed on an exporter. The exporter interacts with a
  device through its exposed interfaces.

* `Client`: The library that connects to the server and leases exporters.
  The client can interact with the leased exporters through the exporter.

* `Controller`: The central service that authenticates and connects the exporters
  and clients, manages leases, and provides an inventory of available exporters
  and clients.

* `Router`: The service that handles routing of messages between clients and
  exporters once they are authenticated by the controller.

## Concepts

* `Lease`: A time-limited reservation of a exporter, a lease is created by a client
  and allows the client to access the exported interfaces for a period of time.

* `Driver`: A class that is defined to interact with a specific type of interface
  exposed by the exporter to the client.
