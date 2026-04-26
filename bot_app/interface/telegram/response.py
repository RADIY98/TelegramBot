from starlette.responses import JSONResponse
import json

from bot_app.domain.response_resolver import IResponseResolver


class TelegramResponseResolver(IResponseResolver):

    @staticmethod
    def send_full_response(params: dict):
        """Send response with msg"""
        return JSONResponse(
                content={
                    "ok": True,
                    "chat_id": params.get("user_id"),
                    "text": params.get("msg"),
                    "reply_markup": json.dumps({'keyboard': params.get("key_board")})
                }
            )

    @staticmethod
    def send_short_response():
        return JSONResponse(
                content={
                    "ok": True
                }
            )
