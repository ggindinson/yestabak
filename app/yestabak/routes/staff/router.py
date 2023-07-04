from aiogram import Router

from yestabak.middlewares.admin_middleware import AdminMiddleware


staffRouter = Router()
staffRouter.message.middleware(AdminMiddleware())
staffRouter.callback_query.middleware(AdminMiddleware())
