from fastapi import FastAPI, Request

def create_app(bot):

    app = FastAPI()

    @app.post("/telegram/webhook")
    async def telegram_webhook(request: Request):
        return await bot.handle_webhook(request)

    return app
