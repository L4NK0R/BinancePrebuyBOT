from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.start_keyboard import inline_keyboard_cryptos, inline_yes_no, inline_keyboard_fiat_crypto, again
from common import cryptos, GetPrice, floatChecker

router_crypto = Router()

class Crypto_chooser(StatesGroup):
    choosing_crypto_crypto = State()
    cont_crypto = State()
    choosing_amount_crypto = State()
    chosen_crypto_abbr_crypto = State()

@router_crypto.callback_query(Text("Crypto"))
async def crypto_board(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы выбрали Crypto\nБудем переводить рубли в крипту",
        reply_markup= await inline_keyboard_cryptos()
    )
    await state.set_state(Crypto_chooser.choosing_crypto_crypto)
    await callback.answer()

@router_crypto.callback_query(Text("Cancel"), Crypto_chooser.choosing_crypto_crypto)
async def a(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "RUB => из рублей в крипту\nCrypto => из крипты в рубли",
        reply_markup= await inline_keyboard_fiat_crypto()
    )
    await state.clear()
    await callback.answer()

@router_crypto.callback_query(Crypto_chooser.choosing_crypto_crypto)
async def choosing_crypto(callback: types.CallbackQuery, state: FSMContext):
    if callback.data in cryptos[0]:
        chosen_crypto = cryptos[1][cryptos[0].index(callback.data)]
        await callback.message.edit_text(
            f"Вы выбрали {callback.data} ({chosen_crypto})\nПродолжим?",
            reply_markup= await inline_yes_no()
        )
        await state.update_data(chosen_crypto=chosen_crypto, chosen_crypto_abbr=callback.data)
        await state.set_state(Crypto_chooser.cont_crypto)
    
    await callback.answer()

@router_crypto.callback_query(Text("Cancel"), Crypto_chooser.cont_crypto)
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы выбрали Crypto\nБудем переводить рубли в крипту",
        reply_markup= await inline_keyboard_cryptos()
    )
    await state.set_state(Crypto_chooser.choosing_crypto_crypto)
    await callback.answer()

@router_crypto.callback_query(Text("Continue"), Crypto_chooser.cont_crypto)
async def answered(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Хорошо\nВведите сумму"
    )
    
    await state.set_state(Crypto_chooser.choosing_amount_crypto)
    await callback.answer()

@router_crypto.message(F.text, Crypto_chooser.choosing_amount_crypto)
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
        await state.update_data(amount=entered_text)
        priceForCrypto = await GetPrice(user_data["chosen_crypto_abbr"])
        usd = await GetPrice("RUB")
        if user_data["chosen_crypto_abbr"] == 'BUSD':
            await message.answer(
                text = f"Рублей- {user_data['amount']}\nИтоговая сумма {user_data['chosen_crypto_abbr'].upper()} будет равна {float(user_data['amount']) / float(usd)}\n\n\nКурс {user_data['chosen_crypto_abbr']} = {usd} рублей", reply_markup= await again()
            )
        else:
            await message.answer(
                text = f"Рублей - {user_data['amount']}\nИтоговая сумма {user_data['chosen_crypto'].upper()} будет равна {(float(user_data['amount'])/float(usd)) / float(priceForCrypto)}\n\n\nКурс {user_data['chosen_crypto_abbr']} = {priceForCrypto} BUSD", reply_markup= await again()
            )
        await state.clear()
