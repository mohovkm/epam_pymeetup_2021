import azure.functions as func
from functions import process_send_message


async def main(queue: func.QueueMessage) -> str:

    await process_send_message.recieve_message_and_notify(queue)
