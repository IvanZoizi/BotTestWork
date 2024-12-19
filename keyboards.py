from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


class DeleteCallback(CallbackData, prefix="delete"):
    id: int


class ListCallback(CallbackData, prefix='list'):
    num: int


def start_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Добавить задачу', callback_data='new'))
    builder.row(types.InlineKeyboardButton(text="Мои задачи", callback_data='my'))
    return builder.as_markup()


def task_kb(data, num):
    builder = InlineKeyboardBuilder()
    res = []
    if num != 0:
        res.append(types.InlineKeyboardButton(text='Назад', callback_data=ListCallback(num=num - 1).pack()))
    if num != (len(data) - 1):
        res.append(types.InlineKeyboardButton(text='Далее', callback_data=ListCallback(num=num + 1).pack()))
    builder.row(*res)
    builder.row(types.InlineKeyboardButton(text='Удалить', callback_data=DeleteCallback(id=data[num][0]).pack()))
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data='start'))
    return builder.as_markup()
