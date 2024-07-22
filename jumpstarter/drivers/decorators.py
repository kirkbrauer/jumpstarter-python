from dataclasses import asdict, is_dataclass
from typing import Final
from uuid import uuid4

from google.protobuf import json_format, struct_pb2

from jumpstarter.common.streams import (
    forward_server_stream,
)
from jumpstarter.v1 import jumpstarter_pb2

MARKER_MAGIC: Final[str] = "07c9b9cc"
MARKER_DRIVERCALL: Final[str] = "marker_drivercall"
MARKER_STREAMCALL: Final[str] = "marker_streamcall"
MARKER_STREAMING_DRIVERCALL: Final[str] = "marker_streamingdrivercall"


def drivercall(func):
    """Mark method as unary drivercall"""

    async def wrapper(self, request, context):
        args = [json_format.MessageToDict(arg) for arg in request.args]

        result = await func(self, *args)

        return jumpstarter_pb2.DriverCallResponse(
            uuid=str(uuid4()),
            result=json_format.ParseDict(asdict(result) if is_dataclass(result) else result, struct_pb2.Value()),
        )

    setattr(wrapper, MARKER_DRIVERCALL, MARKER_MAGIC)

    return wrapper


def streamcall(func):
    """Mark method as streamcall"""

    async def wrapper(self, request_iterator, context):
        async with func(self) as stream:
            async for v in forward_server_stream(request_iterator, stream):
                yield v

    setattr(wrapper, MARKER_STREAMCALL, MARKER_MAGIC)

    return wrapper


def streamingdrivercall(func):
    """Mark method as streaming drivercall"""

    async def wrapper(self, request, context):
        args = [json_format.MessageToDict(arg) for arg in request.args]

        async for result in func(self, *args):
            yield jumpstarter_pb2.StreamingDriverCallResponse(
                uuid=str(uuid4()),
                result=json_format.ParseDict(
                    asdict(result) if is_dataclass(result) else result,
                    struct_pb2.Value(),
                ),
            )

    setattr(wrapper, MARKER_STREAMING_DRIVERCALL, MARKER_MAGIC)

    return wrapper
