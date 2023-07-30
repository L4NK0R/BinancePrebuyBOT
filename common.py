import requests

cryptos = [
    ["XMR","BTC","ZEC","ETH","BCH","BUSD"],
    ["Monero","Bitcoin","ZCash","Ethereum","BitcoinCash","BinanceUSD"]
]

async def GetPrice(a):
    url = "https://api.binance.com/api/v3/ticker/price"
    if a == "BUSD":
        symbol = "BUSDRUB"
    else:
        symbol = a + "BUSD"
    response = requests.get(url, params={'symbol': symbol})
    if response.status_code == 200:
        data = response.json()
        crypto_price = data['price']
        return round(float(crypto_price), 3)
    else:
        return f"Ошибка запроса: {response.status_code}"

async def floatChecker(a):
    if "," in a:
        a = a.replace(",", ".")
        if a.count(".") > 1:
            return "F"
        else:
            try:
                return a
            except ValueError:
                return "F"
    else:
        if a.count(".") > 1:
            return "F"
        else:
            try:
                return a
            except ValueError:
                return "F"
