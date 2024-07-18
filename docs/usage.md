# Jumpstarter Usage

## Subcommands

### Version

```bash
$ jmp version
Jumpstarter CLI from /workspaces/jumpstarter-python/jumpstarter (Python 3.11.9 (main, Jul  2 2024, 21:27:27) [GCC 12.2.0])

Client Version: v0.1.0
Server Version: v0.1.0
Protocol Version: v1alpha1
```

### Client

```bash
$ jmp client create my-client
Enter the server: grpcs://jumpstarter.my-lab.com:1443
Requesting a new token...
Detected kubectl installation
Creating token...

Created my-client
```

Creates a new client `my-client` 

```bash
$ jmp client create my-client -o my-client.yaml
Enter the server: grpcs://jumpstarter.my-lab.com:1443
Requesting a new token...
Detected kubectl installation
Creating token...

Created my-client.yaml
```

Creates a new client configuration YAML file.

```bash
$ jmp client ping
Using client 'default'
Ping grpcs://jumpstarter.my-lab.com:1443 (123.456.789.1)
Pong in 12ms
Pong in 14ms
Pong in 13ms
```

Pings the configured server for a specified client (or default).

```bash
$ jmp client test my-client
Using client 'my-cleint'
Testing connection to grpcs://jumpstarter.my-lab.com:1443 (123.456.789.1)...
Latency 12ms
Connection Successful!
```

Tests the connection for the configured server for a specified client (or default).

### Exporter

```bash
$ jmp exporter create my-exporter -o my-exporter.yaml
Enter the server: grpcs://jumpstarter.my-lab.com:1443
Requesting a new token...
Detected kubectl installation
Creating token...

Created my-exporter.yaml
```

Creates a local exporter configuration YAML file.

```bash
$ jmp exporter start
Exporter 'default' started
```

Starts the default exporter instance as a process in the current terminal.

```bash
$ jmp exporter start my-exporter
Exporter 'default' started
```

Starts the specified exporter instance as a process in the current terminal.

```bash
$ jmp exporter start my-exporter --container
Starting container 'my-exporter' with Podman...
Container Started!
```

Starts the specified exporter instance as a container using Podman/Docker.

```bash
$ jmp exporter start my-exporter --service
Starting service 'my-exporter.service' with systemd...
Service Started!
```

Starts the specified exporter instance as a systemd service.

### Config

```bash
$ jmp config set-exporter my-exporter.yaml
Set default exporter to 'my-exporter'
```

Sets the default exporter config in the `~/.config/jumpstarter`.

### Start

```bash
$ jmp start pytest ./my_test.py
Starting exporter 'default' locally...
...
```

Starts a local exporter instance and runs any test commands passed in as an argument.

### Run

```bash
$ jmp run ./my_test.yaml
Running tests in ./my_test.yaml...
```

Runs a Jumpstarter test defined in YAML.

### Up

```bash
$ jmp up
Detected kubectl installation
Client Version: v1.26.1
Kustomize Version: v4.5.7
Server Version: v1.22.11
Installing Jumpstarter CRDs...
Starting Jumpstarter service...
Jumpstarter started successfully!
```

Starts a local instance of Jumpstarter within the k8s cluster using the current `kubeconfig` and active context.

## Administrator Tasks

### Creating a client token and configuration

```bash
jumpstarter client create my-client -o my-client.yaml
```

This creates a client named `my-client` and outputs the configuration to a YAML
file called `my-client.yaml`:

```yaml
client:
    name: my-client
    endpoint: "grpcs://jumpstarter.my-lab.com:1443"
    token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
```

### Creating a exporter

To connect a device to Jumpstarter, an exporter instance must be registered.

Exporter creation must be done by an administrator user who has access to
the Kubernetes cluster where the `jumpstarter-controller` service is hosted.

```bash
# Specify the location of the kubeconfig to use
export KUBECONFIG=/path/to/kubeconfig
# Create the exporter instance
jumpstarter exporter create my-exporter -o my-exporter.yaml
```

This creates an exporter named `my-exporter` and outputs the configuration to a
YAML file called `my-exporter.yaml`:

```yaml
exporter:
    name: my-exporter
    endpoint: "grpcs://jumpstarter.my-lab.com:1443"
    token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
    # environmentConfig: /etc/jumpstarter/environment.py
```

Creating an exporter registers the custom resource object in the k8s API, the
`jumpstarter-controller` will create an authentication token and attach it to
the object.

### Running an Exporter

The exporter service can be run as a container either within the same cluster
(using node affinity) or on a remote machine that has access to the cluster over
the network.

#### Running using Podman

To run the exporter container on a test runner using Podman:

```bash
# Must be run as privileged to access hardware
podman run --cap-add=all --privileged \
        -v /dev:/dev -v /lib/modules:/lib/modules -v /etc/jumpstarter/:/etc/jumpstarter \
        quay.io/jumpstarter-dev/exporter -c my-exporter.yaml

# additional flags like could be necessary depending on the drivers:
#  --security-opt label=disable
#  --security-opt seccomp=unconfined
```

#### Running as a Service

To run the exporter as a service on a test runner with Jumpstarter installed:

```bash
jumpstarter config set-exporter my-exporter
sudo systemctl start jumpstarter 
```

<!-- TODO: create instructions to setup as quadlets with podman and systemd 
https://www.redhat.com/sysadmin/quadlet-podman -->

## Developer Tasks

### Running tests through a central server

When client configuration exists, Jumpstarter will use the specified endpoint
and token to authenticate with that server

#### Configuration

By default the libraries and CLI will look for a `~/.config/jumpstarter/client.yaml`
file, which contains the endpoint and token to authenticate with the Jumpstarter
service.

Alternatively the client can receive the endpoint and token as environment variables:

```bash
export JUMPSTARTER_ENDPOINT=grpcs://jumpstarter.my-lab.com:1443
export JUMPSTARTER_TOKEN=dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
```

This is useful for CI/CD systems that inject the environment variables into the pipeline.

A custom location to the client configuration can also be passed using the following
environment variable. This is useful in situations where there are multiple client
configurations or in an environment when the config is mounted as a file.

```bash
export JUMPSTARTER_CONFIG=/etc/jumpstarter/my-client.yaml
```

### Running tests locally (without a server)

When no client configuration or environment variables are set, the client will
run in local mode and create an exporter instance to interact with the hardware.

Communication between the local client and exporter take place over a local
socket: `/var/run/jumpstarter.sock`.

A local instance of the exporter can also be started using the following command:

```bash
systemctl start jumpstarter-exporter
```
