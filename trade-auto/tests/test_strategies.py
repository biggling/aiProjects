"""Tests for trading strategies using synthetic data."""

import numpy as np
import pandas as pd
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.strategies import grid, mean_reversion, momentum


def make_ohlcv(prices: list[float]) -> pd.DataFrame:
    """Create a minimal OHLCV DataFrame from a list of close prices."""
    n = len(prices)
    return pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": [1000.0] * n,
    })


def make_oscillating(center: float = 50000, amplitude: float = 5000, periods: int = 500) -> pd.DataFrame:
    """Create oscillating price data (good for grid + mean reversion)."""
    t = np.linspace(0, 10 * np.pi, periods)
    prices = center + amplitude * np.sin(t) + np.random.normal(0, 200, periods)
    return make_ohlcv(prices.tolist())


def make_trending(start: float = 30000, end: float = 60000, periods: int = 500) -> pd.DataFrame:
    """Create trending price data (good for momentum)."""
    trend = np.linspace(start, end, periods)
    noise = np.random.normal(0, 300, periods)
    prices = trend + noise
    return make_ohlcv(prices.tolist())


class TestGridStrategy:
    def test_returns_valid_results(self):
        df = make_oscillating()
        result = grid.run_backtest(df)
        assert "strategy" in result
        assert result["strategy"] == "Grid Trading"
        assert "total_return_pct" in result
        assert "max_drawdown_pct" in result
        assert "total_trades" in result
        assert result["initial_capital"] == 10_000.0

    def test_oscillating_market_generates_trades(self):
        df = make_oscillating()
        result = grid.run_backtest(df)
        assert result["total_trades"] > 0

    def test_custom_params(self):
        df = make_oscillating()
        result = grid.run_backtest(df, num_grids=10, range_pct=0.30, capital=5000)
        assert result["initial_capital"] == 5000


class TestMeanReversionStrategy:
    def test_returns_valid_results(self):
        df = make_oscillating(periods=1000)
        result = mean_reversion.run_backtest(df)
        assert result["strategy"] == "Mean Reversion (RSI + BB)"
        assert "win_rate_pct" in result
        assert "total_return_pct" in result

    def test_has_expected_fields(self):
        df = make_oscillating(periods=1000)
        result = mean_reversion.run_backtest(df)
        assert "wins" in result
        assert "losses" in result
        assert "params" in result
        assert result["params"]["rsi_period"] == 14


class TestMomentumStrategy:
    def test_returns_valid_results(self):
        df = make_trending(periods=1000)
        result = momentum.run_backtest(df)
        assert result["strategy"] == "Momentum (EMA Crossover + MACD)"
        assert "win_rate_pct" in result

    def test_trending_market_has_trades(self):
        df = make_trending(periods=1000)
        result = momentum.run_backtest(df)
        assert result["total_trades"] > 0

    def test_custom_params(self):
        df = make_trending(periods=1000)
        result = momentum.run_backtest(df, fast_ema=8, slow_ema=21, trailing_stop_pct=0.03)
        assert result["params"]["fast_ema"] == 8
        assert result["params"]["slow_ema"] == 21
