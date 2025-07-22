from telegram.ext import ApplicationBuilder, BaseHandler


def run(token: str, handlers: list[BaseHandler]) -> None:
    app = ApplicationBuilder().token(token).build()
    app.add_handlers(handlers)
    app.run_polling()
