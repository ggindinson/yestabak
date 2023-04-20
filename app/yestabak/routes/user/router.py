from aiogram import Router
from yestabak.middlewares import TransferCartDataMiddleware

userRouter = Router()
userRouter.callback_query.middleware(TransferCartDataMiddleware())
