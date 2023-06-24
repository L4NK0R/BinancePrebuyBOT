from aiogram import Router, F, types
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.start_keyboard import inline_keyboard_fiat_crypto
from handlers import crypto_handler, fiat_handler

router_start = Router()

@router_start.callback_query(Text("Start"))
async def start(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        "RUB => из крипты в рубли\nCrypto => из рублей в крипту",
        reply_markup= await inline_keyboard_fiat_crypto()
    )
    await callback.answer()

@router_start.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "RUB => из крипты в рубли\nCrypto => из рублей в крипту",
        reply_markup= await inline_keyboard_fiat_crypto()
    )

@router_start.message(Command("help"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"С помощью этого бота вы можете ввести сумму криптовалюты и узнать ее эквивалентную стоимость в рублях\.\nТакже вы можете указать количество рублей и узнать их эквивалентную стоимость в выбранной вами криптовалюте\.\nВсе курсы обновляются с биржи Binancу\.\nЕсли вы хотите хостить подобного бота на своем сервере, то исходники можете скачать [тут](https://github.com/L4NK0R/BinancePrebuyBOT)\n/start \- начало работы бота\n/help \- вывод этого сообщения", parse_mode="MarkdownV2"
    )
router_start.include_routers(crypto_handler.router_crypto, fiat_handler.router_fiat)
