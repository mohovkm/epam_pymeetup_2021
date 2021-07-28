import json
from unittest.mock import MagicMock, call, patch

import pytest
from functions import process_send_message, setup_email


def test_email_provider_not_known():
    with pytest.raises(KeyError):
        setup_email.send_email("notdefined")


def test_hotmail_provider_assigned():
    func = setup_email.send_email("hotmail")
    assert func is setup_email.hotmail_provider_send_mail


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_out, expected_email, expected_text",
    [
        (
            '{"name":"Mr Nice Guy","email":"mrniceguy@email.com"}',
            "mrniceguy@email.com",
            "Hello, Mr Nice Guy, we recieved your order!",
        )
    ],
)
async def test_recieve_message_and_notify(
    queue_out: str, expected_email: str, expected_text: str
):
    process_send_message.logging = mock_logger = MagicMock()
    send_email = MagicMock()
    queue_mock = MagicMock()
    queue_mock.get_body.decode.return_value = queue_out

    json_mock = MagicMock()
    json_mock.loads.return_value = json.loads(queue_out)

    send_email_function = MagicMock()
    send_email_function.return_value = send_email
    called = [call(expected_email, expected_text)]

    with patch(
        "functions.process_send_message.setup_email.send_email", send_email_function
    ), patch("functions.process_send_message.json", json_mock):
        await process_send_message.recieve_message_and_notify(queue_mock)
        assert send_email.call_args_list == called
        assert mock_logger.info.called


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_out", [('{"name":"Mr Nice Guy","email":"mrniceguy@email.com"}')]
)
async def test_recieve_message_and_notify_fails(queue_out: str):
    mock_logger = MagicMock()
    queue_mock = MagicMock()
    queue_mock.get_body.decode.return_value = queue_out

    json_mock = MagicMock()
    json_mock.loads.return_value = json.loads(queue_out)

    setup_email_mock = MagicMock()
    setup_email_mock.send_email.side_effect = KeyError(
        "Can't find provider name for a not_exists"
    )

    with patch("functions.process_send_message.setup_email", setup_email_mock), patch(
        "functions.process_send_message.logging", mock_logger
    ), patch("functions.process_send_message.json", json_mock):
        called = call(
            "Can't setup email provider: %s",
            KeyError("Can't find provider name for a not_exists"),
        )

        await process_send_message.recieve_message_and_notify(queue_mock)
        assert mock_logger.info.called
        assert mock_logger.error.called
        assert str(mock_logger.error.call_args_list[0]) == str(called)
