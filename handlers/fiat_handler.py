from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.start_keyboard import inline_keyboard_cryptos, inline_yes_no, inline_keyboard_fiat_crypto, again
from common import cryptos, GetPrice, floatChecker

router_fiat = Router()

class Crypto_chooser(StatesGroup):
    choosing_crypto_fiat = State()
    cont_fiat = State()
    choosing_amount_fiat = State()
    chosen_crypto_abbr_fiat = State()

@router_fiat.callback_query(Text("Fiat"))
async def crypto_board(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы выбрали RUB\nБудем переводить крипту в рубли",
        reply_markup= await inline_keyboard_cryptos()
    )
    await state.set_state(Crypto_chooser.choosing_crypto_fiat)
    await callback.answer()

@router_fiat.callback_query(Text("Cancel"), Crypto_chooser.choosing_crypto_fiat)
async def a(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "RUB => из крипты в рубли\nCrypto => из рублей в крипту",
        reply_markup= await inline_keyboard_fiat_crypto()
    )
    await state.clear()
    await callback.answer()

@router_fiat.callback_query(Crypto_chooser.choosing_crypto_fiat)
async def choosing_crypto(callback: types.CallbackQuery, state: FSMContext):
    if callback.data in cryptos[0]:
        chosen_crypto = cryptos[1][cryptos[0].index(callback.data)]
        await callback.message.edit_text(
            f"Вы выбрали {callback.data} ({chosen_crypto})\nПродолжим?",
            reply_markup= await inline_yes_no()
        )
        await state.update_data(chosen_crypto=chosen_crypto, chosen_crypto_abbr=callback.data)
        await state.set_state(Crypto_chooser.cont_fiat)
    
    await callback.answer()

@router_fiat.callback_query(Text("Cancel"), Crypto_chooser.cont_fiat)
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы выбрали RUB\nБудем переводить крипту в рубли",
        reply_markup= await inline_keyboard_cryptos()
    )
    await state.set_state(Crypto_chooser.choosing_crypto_fiat)
    await callback.answer()

@router_fiat.callback_query(Text("Continue"), Crypto_chooser.cont_fiat)
async def answered(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Хорошо\nВведите колличество криптовалюты"
    )
    await state.set_state(Crypto_chooser.choosing_amount_fiat)
    await callback.answer()

@router_fiat.message(F.text, Crypto_chooser.choosing_amount_fiat)
async def amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await message.chat.delete_message(message_id=int(message.message_id - 1))
    await message.delete()
    user_data = await state.get_data()
    entered_text = await floatChecker(user_data["amount"])
    if entered_text == "F":
        await message.answer(text="Вы ввели не верное число, возможно текст\nВведите число")
        await state.update_data(amount="")
    else:
        await state.update_data(amount=entered_text)
        user_data = await state.get_data()
        priceForCrypto = await GetPrice(user_data["chosen_crypto_abbr"])
        usd = await GetPrice("BUSD")
        if user_data["chosen_crypto_abbr"] == 'BUSD':
            await message.answer(
                text = f"{user_data['chosen_crypto_abbr'].upper()} - {user_data['amount']}\nИтоговая сумма в рублях - {round(float(user_data['amount'])*float(priceForCrypto), 2)} рублей\n\n\nКурс {user_data['chosen_crypto_abbr']} = {usd} рублей", reply_markup= await again()
            )
        else:
            await message.answer(
                text = f"{user_data['chosen_crypto_abbr'].upper()} - {user_data['amount']}\nИтоговая сумма в рублях - {round(float(user_data['amount'])*float(priceForCrypto)*usd, 2)} рублей\n\n\nКурс {user_data['chosen_crypto_abbr']} = {priceForCrypto} BUSD", reply_markup= await again()
            )
        await state.clear()
