import yfinance as yf

def get_ticker_object(ticker_symbol):
    return yf.Ticker(ticker_symbol)


def fetch_key_financials(ticker):
    info = ticker.info
    return {
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "ebitda": info.get("ebitda"),
        "revenue": info.get("totalRevenue"),
        "net_income": info.get("netIncomeToCommon"),
    }


def calculate_yoy_revenue_growth(ticker):
    try:
        financials = ticker.financials
        revenue_series = financials.loc["Total Revenue"].sort_index(ascending=False)
        if len(revenue_series) < 2:
            return None
        latest, previous = revenue_series.iloc[0], revenue_series.iloc[1]
        return round(((latest - previous) / previous) * 100, 2)
    except:
        return None


def calculate_5y_price_growth(ticker):
    try:
        hist = ticker.history(period="5y")
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        return round(((end_price - start_price) / start_price) * 100, 2)
    except:
        return None


def get_all_financial_data(ticker_symbol):
    ticker = get_ticker_object(ticker_symbol)
    key_financials = fetch_key_financials(ticker)

    return {
        "market_cap": key_financials.get("market_cap"),
        "pe_ratio": key_financials.get("pe_ratio"),
        "ebitda": key_financials.get("ebitda"),
        "revenue": key_financials.get("revenue"),
        "net_income": key_financials.get("net_income"),
        "yoy_revenue_growth": calculate_yoy_revenue_growth(ticker),
        "price_growth_5y": calculate_5y_price_growth(ticker),
    }


def format_financials_string(financials):
    def safe_format(val):
        return f"{val:,.0f}" if isinstance(val, (int, float)) else "N/A"

    return f"""```
Market Cap: ${safe_format(financials['market_cap'])}
P/E Ratio (TTM): {financials['pe_ratio'] or 'N/A'}
Revenue (TTM): ${safe_format(financials['revenue'])}
Net Income (TTM): ${safe_format(financials['net_income'])}
EBITDA: ${safe_format(financials['ebitda'])}
YoY Revenue Growth: {financials['yoy_revenue_growth']}%
5-Year Stock Price Growth: {financials['price_growth_5y']}%
```"""