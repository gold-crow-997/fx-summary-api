# app/main.py
from fastapi import FastAPI, Query
import requests, json, statistics

app = FastAPI(title="FX Summary API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/summary")
def summary(
    start: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end: str = Query(..., description="End date (YYYY-MM-DD)"),
    breakdown: str = Query("none", description="'daily' or 'none'")
):
    url = f"https://api.frankshar.dev/{start}..{end}?from=EUR&to=USD"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception:
        with open("data/sample_fx.json") as f:
            data = json.load(f)

    rates = [(d["date"], float(d["rate"])) for d in data]
    daily = []

    for i, (date, rate) in enumerate(rates):
        if i == 0:
            pct = None
        else:
            prev = rates[i - 1][1]
            pct = None if prev == 0 else round((rate - prev) / prev * 100, 3)
        if breakdown == "daily":
            daily.append({"date": date, "rate": rate, "pct_change": pct})

    start_rate = rates[0][1]
    end_rate = rates[-1][1]
    mean_rate = round(statistics.mean(r[1] for r in rates), 4)
    total_pct_change = None if start_rate == 0 else round((end_rate - start_rate) / start_rate * 100, 3)

    return {
        "from": start,
        "to": end,
        "start_rate": start_rate,
        "end_rate": end_rate,
        "mean_rate": mean_rate,
        "total_pct_change": total_pct_change,
        "daily": daily if breakdown == "daily" else None,
    }
