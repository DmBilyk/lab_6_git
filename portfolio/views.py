import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio
from .forms import AssetForm
from .services import get_price, MOCK_PRICES, calculate_weights


def dashboard(request):
    portfolios = Portfolio.objects.prefetch_related("assets").all()

    portfolio_data = []
    for portfolio in portfolios:
        assets_raw = [
            {
                "ticker": asset.ticker,
                "quantity": asset.quantity,
                "price": asset.price(),
                "value": asset.current_value(),
            }
            for asset in portfolio.assets.all()
        ]

        # Task 3.1.1: розраховуємо частки для кожного активу
        assets_with_weights = calculate_weights(assets_raw)

        # Task 3.2.2: дані для Chart.js (JSON-серіалізовані для передачі в JS)
        chart_data = {
            "labels": [a["ticker"] for a in assets_with_weights],
            "values": [a["weight"] for a in assets_with_weights],
        }

        portfolio_data.append({
            "portfolio": portfolio,
            "assets": assets_with_weights,
            "total": portfolio.total_value(),
            "chart_data": json.dumps(chart_data),
        })

    return render(request, "portfolio_app/dashboard.html", {"portfolio_data": portfolio_data})


def add_asset(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.portfolio = portfolio
            asset.save()
            return redirect("dashboard")
    else:
        form = AssetForm()

    context = {
        "form": form,
        "portfolio": portfolio,
        "available_tickers": sorted(MOCK_PRICES.keys()),
    }
    return render(request, "portfolio_app/add_asset.html", context)


def create_portfolio(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Portfolio.objects.create(name=name)
        return redirect("dashboard")

    return render(request, "portfolio_app/create_portfolio.html")