import pywifi
import time
import csv
from datetime import datetime
import speedtest

def get_wifi_info():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    time.sleep(3)
    results = iface.scan_results()

    wifi_data = []
    for network in results:
        ssid = network.ssid
        signal = network.signal
        frequency = network.freq
        mac = network.bssid

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

def get_speedtest_results():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000
        return round(download, 2), round(upload, 2)
    except Exception as e:
        print("Speedtest failed:", e)
        return None, None

def write_to_csv(wifi_data, download_speed, upload_speed, filename="wifi_speed_log.csv"):
    file_exists = False
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "ssid", "bssid", "rssi", "frequency_mhz", "ghz_band", "download_mbps", "upload_mbps"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in wifi_data:
            row["download_mbps"] = download_speed
            row["upload_mbps"] = upload_speed
            writer.writerow(row)

def main():
    print("Wi-Fiスキャン + 通信速度測定を1分ごとに開始（Ctrl+Cで終了）")
    try:
        while True:
            wifi_data = get_wifi_info()
            download, upload = get_speedtest_results()
            write_to_csv(wifi_data, download, upload)
            print(f"{len(wifi_data)}件のWi-Fiデータ + 通信速度を記録しました")
            time.sleep(60)
    except KeyboardInterrupt:
        print("ログ記録を終了しました")

if __name__ == "__main__":
    main()
