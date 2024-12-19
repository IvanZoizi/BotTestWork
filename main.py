import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import *
from keyboards import *
from databases import Database
from users import user_handler
from states import *

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"), StateFilter('*'))
async def cmd_start(message: types.Message, state: FSMContext, dbase: Database):
    await state.clear()
    if dbase.get_user(message.from_user.id):
        await message.answer(
            "Привет, выбери, что ты хочешь",
            reply_markup=start_kb()
        )
    else:
        await state.set_state(NewUserState.name)
        await message.answer("Введите свое имя")


@dp.callback_query(F.data == 'start', StateFilter('*'))
async def start_cal(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()
    await call.message.answer(
        "Привет, найду информацию и расскажу об услуге!",
        reply_markup=start_kb()
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(user_handler.router)
    dbase = Database('./db.sqlite')
    await dp.start_polling(bot, dbase=dbase)


if __name__ == "__main__":
    asyncio.run(main())