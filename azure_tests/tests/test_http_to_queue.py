from typing import Dict

import pytest
from functions import process_queue_in


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

    def get_json(self):
        return self.params


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
    request.params = request_body
    result = await process_queue_in.send_message_to_queue(request, queue)
    assert result.text == expected_http
    assert queue.get() == expected_queue
