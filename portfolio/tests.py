from django.test import TestCase
from .services import calculate_weights


class CalculateWeightsTest(TestCase):

    def test_weights_sum_to_100(self):
        """Сума всіх часток має дорівнювати 100%."""
        assets = [
            {"ticker": "AAPL", "value": 1893.0},
            {"ticker": "TSLA", "value": 1775.0},
            {"ticker": "MSFT", "value": 4158.0},
        ]
        result = calculate_weights(assets)
        total_weight = sum(a["weight"] for a in result)
        self.assertAlmostEqual(total_weight, 100.0, places=1)

    def test_single_asset_is_100_percent(self):
        """Єдиний актив має вагу 100%."""
        assets = [{"ticker": "NVDA", "value": 8750.0}]
        result = calculate_weights(assets)
        self.assertEqual(result[0]["weight"], 100.0)

    def test_equal_assets_have_equal_weights(self):
        """Два однакових за вартістю активи мають по 50%."""
        assets = [
            {"ticker": "AAPL", "value": 500.0},
            {"ticker": "TSLA", "value": 500.0},
        ]
        result = calculate_weights(assets)
        self.assertEqual(result[0]["weight"], 50.0)
        self.assertEqual(result[1]["weight"], 50.0)

    def test_empty_portfolio_returns_empty_list(self):
        """Порожній список активів повертає порожній список."""
        result = calculate_weights([])
        self.assertEqual(result, [])

    def test_zero_value_assets_return_zero_weights(self):
        """Якщо всі активи мають нульову вартість — всі ваги 0.0."""
        assets = [
            {"ticker": "AAPL", "value": 0.0},
            {"ticker": "TSLA", "value": 0.0},
        ]
        result = calculate_weights(assets)
        for asset in result:
            self.assertEqual(asset["weight"], 0.0)

    def test_original_fields_are_preserved(self):
        """Функція не видаляє існуючі поля словника."""
        assets = [{"ticker": "AAPL", "value": 1000.0, "quantity": 5}]
        result = calculate_weights(assets)
        self.assertIn("ticker", result[0])
        self.assertIn("quantity", result[0])
        self.assertIn("weight", result[0])