import pandas as pd
import matplotlib.pyplot as plt

# CSVファイル読み込み
df = pd.read_csv("wifi_speed_log.csv")

# タイムスタンプをdatetime型に変換
df["timestamp"] = pd.to_datetime(df["timestamp"])

# SSIDごとに色分けしてRSSIグラフ表示
plt.figure(figsize=(12, 6))
for ssid in df["ssid"].unique():
    ssid_data = df[df["ssid"] == ssid]
    plt.plot(ssid_data["timestamp"], ssid_data["rssi"], label=ssid)

plt.title("RSSI (電波強度) の時間変化")
plt.xlabel("時間")
plt.ylabel("RSSI (dBm)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 通信速度（DL/UL）もプロット
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["download_mbps"], label="Download (Mbps)", color='blue')
plt.plot(df["timestamp"], df["upload_mbps"], label="Upload (Mbps)", color='green')
plt.title("通信速度の時間変化")
plt.xlabel("時間")
plt.ylabel("速度 (Mbps)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
