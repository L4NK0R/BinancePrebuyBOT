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
@router.message(Text(text="нет", ignore_case=True))
async def start_answ(message: Message, state: FSMContext):
    if message.text == "нет" or message.text == "Нет":
        await message.answer(
            "Ладно, идем в начало",
            reply_markup=choose_crypto()
        )
        await state.clear()
    else:
# async def cmd_start(message: Message, state: FSMContext):
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
                f"Вы выбрали {crypto} ({selected_crypto})\nПродолжим?",
                reply_markup=yes_no()
            )
            await state.update_data(chosen_crypto=selected_crypto, chosen_crypto_abbr = crypto)
            break


@router.message(Crypto_chooser.choosing_crypto, (Text(text="да", ignore_case=True)))
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



@router.message(F.text, Crypto_chooser.choosing_amount)
async def amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    user_data = await state.get_data()
    priceForCrypto = await GetPrice(user_data["chosen_crypto_abbr"])
    usd = await GetPrice("RUB")
    
    if user_data["chosen_crypto_abbr"] == 'BUSD':
        await message.answer(
            text = f"Покупка {user_data['chosen_crypto_abbr'].upper()} в рублях - {user_data['amount']}\nИтоговая сумма {user_data['chosen_crypto_abbr'].upper()} будет равна {float(user_data['amount']) / float(usd)}\n\n\nКурс {user_data['chosen_crypto_abbr']} = {usd} RUB"
        )
    else:
        await message.answer(
            text = f"Покупка {user_data['chosen_crypto'].upper()} в рублях - {user_data['amount']}\nИтоговая сумма {user_data['chosen_crypto'].upper()} будет равна {(float(user_data['amount'])/float(usd)) / float(priceForCrypto)}\n\n\nКурс {user_data['chosen_crypto_abbr']} = {priceForCrypto} BUSD"
        )
    # await message.answer(
    #     text= f"{usd}, {float(user_data['amount'])}"
    # )
    await state.clear()
    await message.answer(
            "Какую криптовалюту планируете использовать?",
            reply_markup=choose_crypto()
        )
    await state.set_state(Crypto_chooser.choosing_crypto)

async def GetPrice(a):
    url = "https://api.binance.com/api/v3/ticker/price"
    if a == "RUB":
        symbol = "BUSDRUB"
    else:
        symbol = a + "BUSD"
    response = requests.get(url, params={'symbol': symbol})

# Проверьте статус ответа
    if response.status_code == 200:
        # Извлеките данные из JSON-ответа
        data = response.json()
    
        # Получите стоимость XMR
        crypto_price = data['price']
    
        # Выведите стоимость XMR
        return round(float(crypto_price), 3)
    else:
        return f"Ошибка запроса: {response.status_code}"

