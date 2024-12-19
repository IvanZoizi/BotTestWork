import types

from aiogram import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import *
from databases import Database
from states import *


router=Router()


@router.message(StateFilter(NewUserState.name))
async def new_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона")
    await state.set_state(NewUserState.phone)


@router.message(StateFilter(NewUserState.phone))
async def new_phone(message: types.Message, state: FSMContext, dbase: Database):
    phone = message.text.replace(' ', '')
    if (phone.startswith('8') and len(phone) == 11) or (phone.startswith('+7') and len(phone) == 12):
        data = await state.get_data()
        dbase.new_user(message.from_user.id, data['name'], phone)
        await message.answer("Спасибо, теперь выберете, что вы хотите сделать!", reply_markup=start_kb())
        await state.clear()
    else:
        await message.answer("Введите ваш номер телефона. Формат - 8XXXXXXXXXX")


@router.callback_query(F.data == 'new')
async def new(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(NewTaskState.text)
    await call.message.answer("Укажите задачу")


@router.message(StateFilter(NewTaskState.text))
async def get_text_task(message: types.Message, state: FSMContext, dbase: Database):
    await state.clear()
    dbase.new_tasks(message.from_user.id, message.text)
    await message.answer("Успешно!", reply_markup=start_kb())


@router.callback_query(F.data == 'my')
async def my_task(call: types.CallbackQuery, dbase: Database):
    await call.message.delete()
    data = dbase.get_tasks(call.from_user.id)
    if data:
        await call.message.answer(f"Задача 1\n\n{data[0][2]}", reply_markup=task_kb(data, 0))
    else:
        await call.message.answer("Вы пока не добавили задач", reply_markup=start_kb())


@router.callback_query(ListCallback.filter())
async def check_my_task(call: types.CallbackQuery, callback_data: ListCallback, dbase: Database):
    await call.message.delete()
    data = dbase.get_tasks(call.from_user.id)
    await call.message.answer(f"Задача {int(callback_data.num) + 1}\n\n{data[int(callback_data.num)][2]}", reply_markup=task_kb(data, int(callback_data.num)))


@router.callback_query(DeleteCallback.filter())
async def delete_my_task(call: types.CallbackQuery, callback_data: DeleteCallback, dbase: Database):
    await call.message.delete()
    dbase.del_task(callback_data.id)
    data = dbase.get_tasks(call.from_user.id)
    if data:
        await call.message.answer(f"Задача 1\n\n{data[0][2]}", reply_markup=task_kb(data, 0))
    else:
        await call.message.answer("Вы пока не добавили задач", reply_markup=start_kb())
