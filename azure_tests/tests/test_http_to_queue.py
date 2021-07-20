import os
import sys
from typing import Dict

import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import queue_in  # noqa


class MockQueue:
    queue_value: str

    def set(self, value):
        self.queue_value = value

    def get(self):
        return self.queue_value


class MockRequest:
    _params: dict

    def __init__(self, params: dict) -> None:
        self.params = params

    @property
    def prarams(self):
        return self._params

    @prarams.setter
    def prarams(self, value: dict):
        self._params = value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body, expected_queue, expected_http",
    [
        (
            {"name": "vasya"},
            '{"recieved": "vasya"}',
            "Value vasya was set to the queue",
        ),
    ],
)
async def test_queue_in_expected(
    request_body: Dict[str, str], expected_queue: str, expected_http: str
):
    queue = MockQueue()
    request = MockRequest(request_body)
    result = await queue_in.main(request, queue)
    assert result.get_body().decode("utf-8") == expected_http
    assert queue.get() == expected_queue
