"""Spray-window check from Open-Meteo (free, no key). Spraying before rain washes money away."""
import time

import httpx


_cache: dict = {}

WEATHER_ADVICE = {
    "good": {
        "en": "Good window: spray early morning or evening.",
        "te": "పిచికారీకి అనుకూల సమయం: ఉదయం లేదా సాయంత్రం వేళల్లో పిచికారీ చేయండి.",
        "hi": "छिड़काव के लिए अच्छा समय: सुबह या शाम को छिड़काव करें।",
        "ta": "தெளிக்க உகந்த நேரம்: அதிகாலை அல்லது மாலையில் தெளிக்கவும்.",
        "ml": "തളിക്കാൻ നല്ല സമയം: രാവിലെ അല്ലെങ്കിൽ വൈകുന്നേരം തളിക്കുക.",
    },
    "hold": {
        "en": "Hold spraying: rain chance {rain}% or wind {wind} km/h in next 24h.",
        "te": "పిచికారీని వాయిదా వేయండి: రాబోయే 24 గంటల్లో వర్షం అవకాశం {rain}% లేదా గాలి వేగం {wind} కి.మీ/గం.",
        "hi": "छिड़काव रोकें: अगले 24 घंटे में बारिश की संभावना {rain}% या हवा {wind} किमी/घंटा है।",
        "ta": "தெளிப்பதை ஒத்திவையுங்கள்: அடுத்த 24 மணி நேரத்தில் மழை வாய்ப்பு {rain}% அல்லது காற்று {wind} கி.மீ/மணி.",
        "ml": "തളിക്കുന്നത് മാറ്റിവെക്കുക: അടുത്ത 24 മണിക്കൂറിൽ മഴ സാധ്യത {rain}% അല്ലെങ്കിൽ കാറ്റ് {wind} കി.മീ/മണിക്കൂർ.",
    }
}


def spray_window(lat: float, lon: float, lang: str = "en") -> dict | None:
    key = (round(lat, 2), round(lon, 2))
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < 900:
        raw = hit[1]
    else:
        raw = _fetch(lat, lon)
        _cache[key] = (time.time() if raw else time.time() - 600, raw)
    if not raw:
        return None
    res = dict(raw)
    template_key = "good" if res.get("ok_to_spray") else "hold"
    tbl = WEATHER_ADVICE[template_key]
    fmt = tbl.get(lang, tbl["en"])
    fmt_en = tbl["en"]
    res["advice"] = fmt.format(rain=res.get("max_rain_prob", 0), wind=res.get("max_wind_kmh", 0))
    res["advice_en"] = fmt_en.format(rain=res.get("max_rain_prob", 0), wind=res.get("max_wind_kmh", 0))
    return res


def _fetch(lat, lon):
    try:
        r = httpx.get("https://api.open-meteo.com/v1/forecast", timeout=5, params={
            "latitude": lat, "longitude": lon, "forecast_hours": 24, "timezone": "auto",
            "hourly": "precipitation_probability,wind_speed_10m,temperature_2m,relative_humidity_2m",
        })
        h = r.json()["hourly"]
        rain = max(h["precipitation_probability"] or [0])
        wind = max(h["wind_speed_10m"] or [0])
        temp = max(h["temperature_2m"] or [0])
        hum = round(sum(h["relative_humidity_2m"]) / len(h["relative_humidity_2m"]))
        ok = rain < 40 and wind < 15
        return {"ok_to_spray": ok, "max_rain_prob": rain, "max_wind_kmh": wind, "max_temp_c": temp,
                "avg_humidity": hum}
    except Exception as e:
        print("[weather] unavailable:", e)
        return None
