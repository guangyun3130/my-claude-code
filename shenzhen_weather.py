# -*- coding: utf-8 -*-
"""
使用 Open-Meteo 免费天气接口获取深圳今日天气
接口地址: https://api.open-meteo.com/v1/forecast (无需 API Key)
深圳坐标: 22.5431°N, 114.0579°E

注意: 不强制转换 stdout 编码，保持系统默认(GBK)，
      仅使用 GBK 可编码的字符，避免乱码。
"""

import json
import urllib.parse
import urllib.request

# 深圳坐标
LAT = 22.5431
LON = 114.0579

# 天气代码 -> 中文描述
WMO_CODES = {
    0: "晴",
    1: "大致晴朗",
    2: "局部多云",
    3: "阴",
    45: "雾",
    48: "冻雾",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "浓毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "冻雨",
    67: "冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "中阵雨",
    82: "强阵雨",
    85: "小阵雪",
    86: "大阵雪",
    95: "雷暴",
    96: "雷暴伴小冰雹",
    99: "雷暴伴大冰雹",
}


def fetch_weather():
    """请求 Open-Meteo API 获取深圳天气数据"""
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current_weather": "true",
        "hourly": "temperature_2m,relativehumidity_2m,precipitation,weathercode",
        "timezone": "Asia/Shanghai",
        "forecast_days": 1,
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data


def main():
    print("正在获取深圳今日天气...\n")
    data = fetch_weather()

    current = data["current_weather"]
    wmo = current.get("weathercode")
    weather_desc = WMO_CODES.get(wmo, f"未知代码({wmo})")

    print("=" * 40)
    print("[深圳天气]")
    print("=" * 40)
    print(f"时间    : {current['time']}")
    print(f"当前温度 : {current['temperature']} °C")
    print(f"风速    : {current['windspeed']} km/h")
    print(f"风向    : {current['winddirection']}°")
    print(f"天气    : {weather_desc}")

    # 今日逐小时预报摘要
    hourly = data["hourly"]
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    hums = hourly["relativehumidity_2m"]
    preps = hourly["precipitation"]
    codes = hourly["weathercode"]

    print("\n" + "=" * 40)
    print("[今日逐小时预报]（每 3 小时）")
    print("=" * 40)
    for i in range(0, len(times), 3):
        hour = times[i][11:16]
        desc = WMO_CODES.get(codes[i], codes[i])
        print(
            f"  {hour}  {desc:<8} "
            f"{temps[i]:>5.1f}°C  湿度 {hums[i]:>3}%  "
            f"降水 {preps[i]:.1f}mm"
        )

    print("\n数据来源: Open-Meteo (https://open-meteo.com/)")


if __name__ == "__main__":
    main()
