import pywifi
from pywifi import const
import time

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # 最初のWi-Fiインターフェースを取得

    iface.scan()  # スキャンを開始
    time.sleep(3)  # スキャン完了まで待機（3秒程度）
    results = iface.scan_results()

    for network in results:
        ssid = network.ssid
        signal = network.signal  # RSSI（値が大きいほど強い）
        frequency = network.freq  # 周波数（例：2412MHz → 2.4GHz）
        mac = network.bssid

        ghz_band = ""
        if 2400 <= frequency <= 2500:
            ghz_band = "2.4GHz"
        elif 4900 <= frequency <= 5900:
            ghz_band = "5GHz"
        elif 5900 <= frequency <= 7100:
            ghz_band = "6GHz"
        else:
            ghz_band = "不明"

        print(f"SSID: {ssid}, RSSI: {signal}, 周波数: {frequency}MHz ({ghz_band}), BSSID: {mac}")

if __name__ == "__main__":
    scan_wifi()
