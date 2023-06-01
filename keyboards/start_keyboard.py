from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

cryptos = [
    ["XMR","BTC","ZEC","ETH","BCH","BUSD"],
    ["Monero","Bitcoin","ZCash","Etherium","Bitcoin Cash","Binance USD"]
]

def choose_crypto() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for crypto in cryptos[0]:
        kb.button(text=crypto)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

def yes_no() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)