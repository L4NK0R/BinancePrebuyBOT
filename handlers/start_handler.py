from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.start_keyboard import choose_crypto, cryptos, yes_no
import requests

router = Router()

class Crypto_chooser(StatesGroup):
    choosing_crypto = State()
    choosing_amount = State()
    chosen_crypto_abbr = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Какую криптовалюту планируете использовать?",
        reply_markup=choose_crypto()
    )
    await state.set_state(Crypto_chooser.choosing_crypto)

@router.message(F.text.in_(cryptos[0]), Crypto_chooser.choosing_crypto)
async def answer_crypto(message: Message, state: FSMContext):
    for index, crypto in enumerate(cryptos[0]):
        if message.text.upper() == crypto:
            selected_crypto = cryptos[1][index]
            await message.answer(
                f"Вы выбрали {crypto} ({selected_crypto})",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.update_data(chosen_crypto=selected_crypto, chosen_crypto_abbr = crypto)
            break
    await message.answer(
        "Продолжим?",
        reply_markup = yes_no()
    )
    chosen_crypto_abbr = F.text.upper()



router2 = Router()

@router2.message(Crypto_chooser.choosing_crypto, (Text(text="да", ignore_case=True)))
async def answ_yes(message: Message, state: FSMContext):
    # user_data = await state.get_data()
    # await message.answer(
    #     text=f"{user_data}"
    # )
    await state.set_state(Crypto_chooser.choosing_amount)
    await message.answer(
        "Хорошо, введите сумму в рублях",
        reply_markup=ReplyKeyboardRemove()
    )

@router2.message(Text(text="нет", ignore_case=True))
async def answ_no(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Ладно, идем в начало",
        reply_markup=choose_crypto()
    )


@router2.message(F.text, Crypto_chooser.choosing_amount)
async def amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    user_data = await state.get_data()
    usd = 80
    priceForCrypto = GetPrice(user_data['chosen_crypto'])
    await message.answer(
        text = f"Покупка {user_data['chosen_crypto'].upper()} в рублях - {user_data['amount']}\nИтоговая сумма в {user_data['chosen_crypto'].upper()} будет равна {(float(user_data['amount'])/float(usd)) / float(priceForCrypto)}\n\n\nКурс {user_data['chosen_crypto_abbr']} = {priceForCrypto} USD"
    )
    await state.clear()


def GetPrice(a):
    url = "https://api.blockchair.com/"+a.lower()+"/stats"
    data = requests.get(url).text
    # Найти позицию строки "blocks"
    index = data.find('"market_price_usd"')
    if index != -1:
        # Извлечь число справа от строки "blocks"
        start_index = index + len('"market_price_usd":')
        end_index = data.find(',', start_index)
        number = data[start_index:end_index]
        return number
    else:
        return url
