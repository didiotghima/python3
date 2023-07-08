import schedule, requests

def hello_world():
    print("Hello World and Geeks")

def backend_08():
    print("Здраствувйте, у вас сегодня урок в 18:00...")

def get_btc():
    response = requests.get("https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT")
    data = response.json()

    # print(data)
    print(f"Текущий курс биткойна {data.get('price')} $")
# schedule.every(1).second.do(hello_world)
# schedule.every(1).minutes.do(hello_world)
# schedule.every().day.at('18:22').do(hello_world)
# schedule.every().wednesday.at("18:25").do(backend_08)
# schedule.every(10).seconds.do(get_btc)
schedule.every(3).seconds.do(get_btc)

while True:
    schedule.run_pending()
