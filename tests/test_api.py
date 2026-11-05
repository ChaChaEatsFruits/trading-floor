import pytest

from backend import accounts, api
from backend.accounts import Account, Transaction


def tx(symbol, quantity, price):
    return Transaction(symbol=symbol, quantity=quantity, price=price, timestamp="2026-01-01 10:00:00", rationale="test")


def make_account(holdings, transactions, balance=0.0):
    return Account(
        name="test", balance=balance, strategy="", holdings=holdings,
        transactions=transactions, portfolio_value_time_series=[],
    )


def test_average_cost_ignores_sells_and_other_symbols():
    account = make_account(
        {"AAPL": 15},
        [tx("AAPL", 10, 100.0), tx("AAPL", 10, 130.0), tx("AAPL", -5, 150.0), tx("MSFT", 3, 400.0)],
    )
    assert api.average_cost(account, "AAPL") == pytest.approx(115.0)
    assert api.average_cost(account, "TSLA") == 0.0


def test_holdings_detail(monkeypatch):
    monkeypatch.setattr(api.market, "get_share_price", lambda symbol: 120.0)
    account = make_account({"AAPL": 15}, [tx("AAPL", 10, 100.0), tx("AAPL", 10, 130.0), tx("AAPL", -5, 150.0)])
    assert api.holdings_detail(account) == [
        {"symbol": "AAPL", "quantity": 15, "price": 120.0, "avg_cost": pytest.approx(115.0),
         "market_value": 1800.0, "unrealized_pnl": pytest.approx(75.0)}
    ]


def test_buy_rejects_position_over_25_percent(monkeypatch):
    monkeypatch.setattr(accounts, "get_share_price", lambda symbol: 100.0)
    monkeypatch.setattr(Account, "save", lambda self: None)
    monkeypatch.setattr(accounts, "write_log", lambda *a: None)
    account = make_account({}, [], balance=10_000.0)
    with pytest.raises(ValueError, match="at most 25 more"):
        account.buy_shares("AAPL", 26, "too big")
    account.buy_shares("AAPL", 24, "fits")  # 24 * 100.2 spread price < $2,500 cap
    assert account.holdings == {"AAPL": 24}
