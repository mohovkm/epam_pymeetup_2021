import json
from typing import Dict
from unittest.mock import MagicMock, Mock

import pytest
from functions import process_queue_in


class MockQueue:
    queue_value: str

    def __init__(self, value: str = None) -> None:
        self.queue_value = value or ""

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


@pytest.fixture(autouse=True)
def mock_queue():
    return MockQueue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body, expected_queue, expected_http, expected_status_code",
    [
        (
            {"name": "vasya", "email": "vasya@va.sya"},
            {"name": "vasya", "email": "vasya@va.sya"},
            "Value for vasya was set to the queue",
            200,
        ),
    ],
)
async def test_queue_in_expected(
    mock_queue: MockQueue,
    request_body: Dict[str, str],
    expected_queue: str,
    expected_http: str,
    expected_status_code: int,
):
    queue = mock_queue()
    request = MockRequest(request_body)

    result = await process_queue_in.send_message_to_queue(request, queue)

    assert result.text == expected_http
    assert result.status_code == expected_status_code
    assert json.loads(queue.get()) == expected_queue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body, expected_queue, expected_http, expected_status_code",
    [
        (
            {},
            "",
            "You must provide name and email in json body",
            400,
        ),
    ],
)
async def test_queue_in_empty_body(
    mock_queue: MockQueue,
    request_body: Dict[str, str],
    expected_queue: str,
    expected_http: str,
    expected_status_code: int,
):
    queue = mock_queue()
    request = MockRequest(request_body)
    process_queue_in.logging = mock_logging = Mock()

    result = await process_queue_in.send_message_to_queue(request, queue)

    assert result.text == expected_http
    assert result.status_code == expected_status_code
    assert queue.get() == expected_queue
    assert mock_logging.error.called


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body, expected_queue, expected_http, expected_status_code",
    [
        (
            None,
            "",
            "You must provide name and email in json body",
            400,
        ),
    ],
)
async def test_queue_in_very_empty_body(
    mock_queue: MockQueue,
    request_body: Dict[str, str],
    expected_queue: str,
    expected_http: str,
    expected_status_code: int,
):
    queue = mock_queue()
    request = MagicMock()
    request.get_json.side_effect = ValueError()
    process_queue_in.logging = mock_logging = Mock()

    result = await process_queue_in.send_message_to_queue(request, queue)

    assert result.text == expected_http
    assert result.status_code == expected_status_code
    assert queue.get() == expected_queue
    assert mock_logging.error.called
