import pywifi
import time
import csv
from datetime import datetime

def get_wifi_info():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    time.sleep(3)  # スキャン完了までの待機
    results = iface.scan_results()

    wifi_data = []
    for network in results:
        ssid = network.ssid
        signal = network.signal
        frequency = network.freq
        mac = network.bssid

        # GHz帯の判別
        if 2400 <= frequency <= 2500:
            ghz_band = "2.4GHz"
        elif 4900 <= frequency <= 5900:
            ghz_band = "5GHz"
        elif 5900 <= frequency <= 7100:
            ghz_band = "6GHz"
        else:
            ghz_band = "不明"

        wifi_data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ssid": ssid,
            "bssid": mac,
            "rssi": signal,
            "frequency_mhz": frequency,
            "ghz_band": ghz_band
        })

    return wifi_data

def write_to_csv(data, filename="wifi_log.csv"):
    file_exists = False
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "ssid", "bssid", "rssi", "frequency_mhz", "ghz_band"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in data:
            writer.writerow(row)

def main():
    print("Wi-Fiスキャン＆ログ記録を1分ごとに開始します（Ctrl+Cで終了）")
    try:
        while True:
            wifi_data = get_wifi_info()
            write_to_csv(wifi_data)
            print(f"{len(wifi_data)}件のデータを記録しました")
            time.sleep(60)  # 1分待機
    except KeyboardInterrupt:
        print("ログ記録を終了しました")

if __name__ == "__main__":
    main()
