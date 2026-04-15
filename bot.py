import requests
import time

TOKEN = "8741517222:AAG9lxGMxXivRLNytaTknmEEkzSXLFch-hw"
CHAT_ID = "6827512180"

def kirim(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": pesan})

def scan():
    url = "https://scanner.tradingview.com/indonesia/scan"

    payload = {
        "filter": [{"left": "volume", "operation": "nempty"}],
        "options": {"lang": "en"},
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": ["name","close","change","Value.Traded","SMA20","RSI"]
    }

    res = requests.post(url, json=payload)
    data = res.json()

    hasil = []

    for item in data["data"][:50]:
        d = item["d"]

        kode = d[0]
        harga = d[1]
        change = d[2]
        value = d[3]
        sma20 = d[4]
        rsi = d[5]

        if value > 1_000_000_000 and harga > sma20 and 50 < rsi < 65:
            entry = harga
            sl = int(harga * 0.95)
            tp = int(harga * 1.10)

            hasil.append((kode, entry, sl, tp, value))

    if hasil:
        top = sorted(hasil, key=lambda x: x[4], reverse=True)[0]

        pesan = f"""
🔥 SIGNAL SAHAM 🔥
{top[0]}

Entry: {top[1]}
SL: {top[2]}
TP: {top[3]}
"""
        kirim(pesan)

# LOOP AUTO
while True:
    try:
        scan()
        time.sleep(300)  # 5 menit
    except:
        time.sleep(60)