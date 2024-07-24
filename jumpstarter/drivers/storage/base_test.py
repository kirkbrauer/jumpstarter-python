from tempfile import NamedTemporaryFile

import pytest

from jumpstarter.common.grpc import serve
from jumpstarter.drivers.storage import MockStorageMux

pytestmark = pytest.mark.anyio


async def test_drivers_mock_storage_mux():
    async with serve(MockStorageMux(name="storage")) as client:
        with NamedTemporaryFile(delete_on_close=False) as file:
            file.write(b"testcontent" * 1000)
            file.close()

            async with client.local_file(file.name) as handle:
                await client.write(handle)