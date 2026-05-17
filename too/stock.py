import yfinance as yf

def get_stock(symbol: str):

    stock = yf.Ticker(symbol)
    hist = stock.history(period="5d")

    if hist.empty:
        return None

    latest_price = hist["Close"].iloc[-1]
    prev_price = hist["Close"].iloc[-2]

    change = ((latest_price - prev_price) / prev_price) * 100

    return {
        "symbol": symbol,
        "price": round(latest_price, 2),
        "change_pct": round(change, 2)
    }
