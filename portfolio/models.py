from django.db import models
from .services import get_price, calculate_asset_value


class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_value(self) -> float:
        """FIX BUG 3: повертає 0.0 для порожнього портфеля замість ZeroDivisionError."""
        assets = self.assets.all()
        if not assets.exists():
            return 0.0
        return sum(asset.current_value() for asset in assets)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"


class Asset(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="assets"
    )
    ticker = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()  # FIX BUG 1: PositiveIntegerField не дозволяє від'ємні значення на рівні БД

    def __str__(self):
        return f"{self.ticker} ({self.quantity})"

    def price(self) -> float:

        return get_price(self.ticker)

    def current_value(self) -> float:

        return calculate_asset_value(self.ticker, self.quantity)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"