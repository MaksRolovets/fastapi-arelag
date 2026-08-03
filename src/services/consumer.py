class ConsumerService:

    @staticmethod
    async def process(event: dict) -> None:
        print(event)

        