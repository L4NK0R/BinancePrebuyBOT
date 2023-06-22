from aiogram import types

async def inline_keyboard_cryptos():
    buttons = [
        [
            types.InlineKeyboardButton(text="XMR", callback_data="XMR"),
            types.InlineKeyboardButton(text="ZEC", callback_data="ZEC"),
            types.InlineKeyboardButton(text="BTC", callback_data="BTC"),
        ],
        [
            types.InlineKeyboardButton(text="ETH", callback_data="ETH"),
            types.InlineKeyboardButton(text="BCH", callback_data="BCH"),
            types.InlineKeyboardButton(text="BUSD", callback_data="BUSD"),
        ],[types.InlineKeyboardButton(text="Отмена", callback_data="Cancel")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb


async def inline_yes_no():
    buttons = [
        [
            types.InlineKeyboardButton(text="Да", callback_data="Continue")
        ],
        [
            types.InlineKeyboardButton(text="Нет", callback_data="Cancel")
        ]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
        
async def inline_keyboard_fiat_crypto():
    buttons = [
        [
            types.InlineKeyboardButton(text="RUB", callback_data="Fiat"),
            types.InlineKeyboardButton(text="Crypto", callback_data="Crypto")
        ]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def again():
    buttons = [
        [
            types.InlineKeyboardButton(text="Начать заново", callback_data="Start")
        ]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
