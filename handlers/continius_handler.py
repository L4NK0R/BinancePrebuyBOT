# from aiogram import Router, F
# from aiogram.filters import Command
# from aiogram.filters.text import Text
# from aiogram.types import Message, ReplyKeyboardRemove
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State


# from keyboards.start_keyboard import choose_crypto, yes_no, cryptos
# router2 = Router()


# @router2.message(Text(text="да", ignore_case=True))
# async def answ_yes(message: Message):
#     await message.answer(
#         "Хорошо, введите сумму",
#         reply_markup=ReplyKeyboardRemove()
#     )
# @router2.message(Text(text="нет", ignore_case=True))
# async def answ_no(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         "Ладно, идем в начало",
#         reply_markup=choose_crypto()
#     )
