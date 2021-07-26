import json
from typing import List
from unittest.mock import MagicMock, Mock

import pytest
from functions import process_send_grid_message
from pydantic import BaseModel, validator


class ToEmail(BaseModel):
    email: str


class Personaliztions(BaseModel):
    to: List[ToEmail]


class Content(BaseModel):
    type: str
    value: str

    @validator("type")
    def type_must_be_text_plain(cls, value):
        assert value == "text/plain", 'type must be set to "text/plain"'
        return value


class Message(BaseModel):
    personalizations: List[Personaliztions]
    subject: str
    content: List[Content]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_out, expected_email_json",
    [
        (
            '{"name":"Mr Nice Guy","email":"mrniceguy@email.com"}',
            {
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": "mrniceguy@email.com",
                            },
                        ],
                    },
                ],
                "subject": "Azure Functions email with SendGrid",
                "content": [
                    {
                        "type": "text/plain",
                        "value": "Hello, Mr Nice Guy, we recieved your order!",
                    },
                ],
            },
        )
    ],
)
async def test_queue_to_email_expected(queue_out: str, expected_email_json: dict):
    message_structure = {}

    def set_message_structure(value):
        nonlocal message_structure
        message_structure = json.loads(value)

    sendGridMessage = MagicMock(name="sendGridMessage")
    sendGridMessage.set = set_message_structure
    process_send_grid_message.logging = mock_logger = Mock()

    await process_send_grid_message.recieve_message_and_notify(
        queue_out, sendGridMessage
    )

    assert mock_logger.info.called

    # First way of checking
    pydantic_message = Message(**message_structure)

    # Second way of checking
    assert pydantic_message.dict()["personalizations"][0]["to"] == [
        {"email": "mrniceguy@email.com"}
    ]

    # Third way (usual) of checking
    assert message_structure == expected_email_json
