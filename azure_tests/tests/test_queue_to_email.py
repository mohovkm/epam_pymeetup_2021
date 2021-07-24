import json
from typing import List
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, validator

from functions import process_send_message


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
            '{"data":"message from the queue"}',
            {
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": "konstantin_mokhov@epam.com",
                            },
                        ],
                    },
                ],
                "subject": "Azure Functions email with SendGrid",
                "content": [
                    {
                        "type": "text/plain",
                        "value": 'Sent from Azure Functions. Value from the queue: {"data":"message from the queue"}',
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

    queue = MagicMock()
    queue.get.return_value = queue_out

    await process_send_message.recieve_message_and_notify(queue, sendGridMessage)

    assert queue.get.called is True

    # First way of checking
    pydantic_message = Message(**message_structure)

    # Second way of checking
    assert pydantic_message.dict()["personalizations"][0]["to"] == [
        {"email": "konstantin_mokhov@epam.com"}
    ]

    # Third way (usual) of checking
    assert message_structure == expected_email_json
