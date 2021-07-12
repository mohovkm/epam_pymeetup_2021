import validators
from aiohttp import ClientSession, ClientTimeout


class CustomLogicException(Exception):
    """Exception to flag, that something wrong happened with CustomLogic class"""


class CustomLogic:
    def __init__(self, url: str) -> None:
        if not validators.url(url):
            raise CustomLogicException("Wrong url.")

        self.url = url

    async def query_data(self) -> str:
        """This function queries provided url

        Returns:
            str: Human-readable response with status code
        """
        timeout = ClientTimeout(total=5)
        async with ClientSession(timeout=timeout) as session:
            result = await session.get(self.url)

            if not result.ok:
                return f"Url answered with error: {result.status}, {result.text}"

            return f"All fine. Returned status_code: {result.status}"
