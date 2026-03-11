

MOCK_PRICES: dict[str, float] = {
    "AAPL": 189.30,
    "TSLA": 177.50,
    "GOOGL": 175.20,
    "MSFT": 415.80,
    "AMZN": 192.40,
    "NVDA": 875.00,
    "META": 520.10,
    "BRK.B": 398.60,
    "JPM": 196.20,
    "V": 278.90,
}

UNKNOWN_PRICE = 0.0


def get_price(ticker: str) -> float:

    return MOCK_PRICES.get(ticker.upper(), UNKNOWN_PRICE)


def calculate_asset_value(ticker: str, quantity: int) -> float:

    return get_price(ticker) * quantity


def calculate_weights(assets: list[dict]) -> list[dict]:

    total = sum(asset["value"] for asset in assets)
    if total == 0:
        return [{**asset, "weight": 0.0} for asset in assets]

    return [
        {**asset, "weight": round(asset["value"] / total * 100, 2)}
        for asset in assets
    ]