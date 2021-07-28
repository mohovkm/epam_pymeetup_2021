from unittest.mock import MagicMock, call, patch

import pytest
from functions import setup_email


@pytest.mark.parametrize(
    "sender_email, receiver_email, smtp_server, smtp_port, smtp_password, text",
    [
        (
            "mrniceguy@email.com",
            "mrbadguy@email.com",
            "smtp_server",
            123,
            "123",
            "my message text",
        ),
    ],
)
def test_hotmail_provider_send_mail_ok(
    sender_email: str,
    receiver_email: str,
    smtp_server: str,
    smtp_port: int,
    smtp_password: str,
    text: str,
):
    getenv_dict = {
        "HOTMAIL_PORT": smtp_port,
        "HOTMAIL_SMTP": smtp_server,
        "HOTMAIL_SENDER": sender_email,
        "HOTMAIL_PASSWORD": "123",
    }

    def getenv_mock(x: str, y=None):
        return getenv_dict[x]

    smtp_mock = MagicMock()
    smtp_instance_mock = MagicMock()
    smtp_mock.SMTP.return_value = smtp_instance_mock
    smtp_server_call = call(smtp_server, smtp_port)
    smtp_login_call = call(sender_email, smtp_password)

    d = {}
    mime_multipart_mock = MagicMock()
    mime_multipart_mock_instance = MagicMock()
    mime_multipart_mock.return_value = mime_multipart_mock_instance
    mime_multipart_mock_instance.__getitem__.side_effect = d.__getitem__
    mime_multipart_mock_instance.__setitem__.side_effect = d.__setitem__
    mime_multipart_mock_instance.__contains__.side_effect = d.__contains__

    mime_text_mock = MagicMock()
    mime_text_mock_call = call(text)

    mime_text_mock_instance = MagicMock()
    mime_text_mock.return_value = mime_text_mock_instance
    multipart_attach_call = call(mime_text_mock_instance)

    sendmail_call = call(
        sender_email, receiver_email, mime_multipart_mock_instance.as_string()
    )

    with patch("functions.setup_email.getenv", getenv_mock), patch(
        "functions.setup_email.smtplib", smtp_mock
    ), patch("functions.setup_email.MIMEMultipart", mime_multipart_mock), patch(
        "functions.setup_email.MIMEText", mime_text_mock
    ):
        setup_email.hotmail_provider_send_mail(receiver_email, text)
        assert smtp_mock.SMTP.call_args_list[0] == smtp_server_call
        assert smtp_instance_mock.starttls.called
        assert smtp_instance_mock.login.call_args_list[0] == smtp_login_call
        assert mime_multipart_mock_instance["From"] == sender_email
        assert mime_multipart_mock_instance["To"] == receiver_email
        assert mime_text_mock.call_args_list[0] == mime_text_mock_call
        assert (
            mime_multipart_mock_instance.attach.call_args_list[0]
            == multipart_attach_call
        )

        assert str(smtp_instance_mock.sendmail.call_args_list[0]) == str(sendmail_call)

        assert smtp_instance_mock.quit.called
