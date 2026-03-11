from django import forms
from .models import Asset
from .services import MOCK_PRICES


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["ticker", "quantity"]
        widgets = {
            "ticker": forms.TextInput(attrs={"placeholder": "напр. AAPL, TSLA, MSFT"}),
            "quantity": forms.NumberInput(attrs={"placeholder": "напр. 10", "min": 1}),
        }

    def clean_quantity(self):
        """FIX BUG 1: забороняємо від'ємну та нульову кількість акцій."""
        quantity = self.cleaned_data.get("quantity")
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError("Кількість акцій має бути більше нуля.")
        return quantity

    def clean_ticker(self):
        ticker = self.cleaned_data.get("ticker", "").upper()
        if ticker not in MOCK_PRICES:
            available = ", ".join(MOCK_PRICES.keys())
            raise forms.ValidationError(
                f"Тікер «{ticker}» не знайдено. Доступні: {available}"
            )
        return ticker