class TelegramBot:

    def __init__(self, pool):
        self.pool = pool

    async def handle_webhook(self, request):
        await request.json()
