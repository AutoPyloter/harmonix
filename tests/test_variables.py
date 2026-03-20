"""
tests/test_variables.py
=======================
Unit tests for harmonix.variables — Continuous, Discrete, Integer, Categorical.
"""

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from harmonix.variables import Continuous, Discrete, Integer, Categorical, _frange


# ---------------------------------------------------------------------------
# _frange helper
# ---------------------------------------------------------------------------

class TestFrange:
    def test_basic(self):
        result = _frange(0.0, 0.5, 2.0)
        assert result == [0.0, 0.5, 1.0, 1.5, 2.0]

    def test_endpoint_always_included(self):
        # (1.0 - 0.0) / 0.3 is not an integer
        result = _frange(0.0, 0.3, 1.0)
        assert result[-1] == 1.0

    def test_single_value(self):
        result = _frange(5.0, 1.0, 5.0)
        assert result == [5.0]

    def test_negative_step_raises(self):
        with pytest.raises(ValueError):
            _frange(0.0, -1.0, 5.0)

    def test_integer_range(self):
        result = _frange(1.0, 1.0, 5.0)
        assert result == [1.0, 2.0, 3.0, 4.0, 5.0]


# ---------------------------------------------------------------------------
# Continuous
# ---------------------------------------------------------------------------

class TestContinuous:
    def test_sample_in_bounds(self):
        v = Continuous(0.0, 1.0)
        for _ in range(100):
            s = v.sample({})
            assert 0.0 <= s <= 1.0

    def test_filter_basic(self):
        v = Continuous(0.0, 5.0)
        candidates = [-1.0, 0.0, 2.5, 5.0, 5.1, 100.0]
        result = v.filter(candidates, {})
        assert result == [0.0, 2.5, 5.0]

    def test_filter_empty(self):
        v = Continuous(10.0, 20.0)
        assert v.filter([1.0, 2.0, 3.0], {}) == []

    def test_neighbor_stays_in_bounds(self):
        v = Continuous(0.0, 1.0)
        random.seed(42)
        for _ in range(200):
            nb = v.neighbor(0.5, {})
            assert 0.0 <= nb <= 1.0

    def test_neighbor_zero_width(self):
        v = Continuous(3.0, 3.0)
        assert v.neighbor(3.0, {}) == 3.0

    def test_dependent_lo(self):
        v = Continuous(lo=lambda ctx: ctx["x"], hi=10.0)
        for _ in range(50):
            x = random.uniform(1.0, 5.0)
            s = v.sample({"x": x})
            assert s >= x

    def test_dependent_hi(self):
        v = Continuous(lo=0.0, hi=lambda ctx: ctx["x"])
        for _ in range(50):
            x = random.uniform(5.0, 10.0)
            s = v.sample({"x": x})
            assert s <= x

    def test_filter_respects_dependent_bounds(self):
        v = Continuous(lo=lambda ctx: ctx["a"], hi=10.0)
        result = v.filter([1.0, 3.0, 5.0, 12.0], {"a": 3.0})
        assert result == [3.0, 5.0]


# ---------------------------------------------------------------------------
# Discrete
# ---------------------------------------------------------------------------

class TestDiscrete:
    def test_sample_on_grid(self):
        v = Discrete(0.0, 0.5, 2.0)
        grid = {0.0, 0.5, 1.0, 1.5, 2.0}
        for _ in range(100):
            s = v.sample({})
            assert any(abs(s - g) < 1e-9 for g in grid)

    def test_filter_keeps_grid_values(self):
        v = Discrete(0.0, 1.0, 5.0)
        candidates = [0.0, 1.0, 1.5, 2.0, 5.0, 6.0]
        result = v.filter(candidates, {})
        assert set(result) == {0.0, 1.0, 2.0, 5.0}

    def test_filter_float_tolerance(self):
        # 0.1 + 0.2 in floating point is not exactly 0.3
        v = Discrete(0.0, 0.1, 1.0)
        tricky = 0.1 + 0.2   # ~0.30000000000000004
        result = v.filter([tricky], {})
        # Should still be kept because it's within tolerance of 0.3
        assert len(result) == 1

    def test_neighbor_steps(self):
        v = Discrete(0.0, 1.0, 4.0)
        nb = v.neighbor(2.0, {})
        assert nb in {1.0, 3.0}

    def test_neighbor_at_lower_bound(self):
        v = Discrete(0.0, 1.0, 4.0)
        nb = v.neighbor(0.0, {})
        assert nb == 1.0

    def test_neighbor_at_upper_bound(self):
        v = Discrete(0.0, 1.0, 4.0)
        nb = v.neighbor(4.0, {})
        assert nb == 3.0

    def test_neighbor_off_grid_unchanged(self):
        v = Discrete(0.0, 1.0, 4.0)
        assert v.neighbor(2.7, {}) == 2.7

    def test_dependent_grid(self):
        v = Discrete(lo=0.0, step=1.0, hi=lambda ctx: ctx["n"])
        grid = v._grid({"n": 3.0})
        assert grid == [0.0, 1.0, 2.0, 3.0]


# ---------------------------------------------------------------------------
# Integer
# ---------------------------------------------------------------------------

class TestInteger:
    def test_sample_is_int(self):
        v = Integer(1, 10)
        for _ in range(50):
            s = v.sample({})
            assert isinstance(s, int)
            assert 1 <= s <= 10

    def test_filter_returns_ints(self):
        v = Integer(1, 5)
        result = v.filter([1, 2, 3, 6, 0], {})
        assert all(isinstance(x, int) for x in result)
        assert set(result) == {1, 2, 3}

    def test_neighbor_is_int(self):
        v = Integer(1, 10)
        for val in range(1, 11):
            nb = v.neighbor(val, {})
            assert isinstance(nb, int)

    def test_neighbor_adjacent(self):
        v = Integer(1, 10)
        nb = v.neighbor(5, {})
        assert nb in {4, 6}

    def test_dependent_hi(self):
        v = Integer(lo=1, hi=lambda ctx: ctx["max_n"])
        s = v.sample({"max_n": 3})
        assert 1 <= s <= 3


# ---------------------------------------------------------------------------
# Categorical
# ---------------------------------------------------------------------------

class TestCategorical:
    def test_sample_in_choices(self):
        choices = ["S235", "S275", "S355"]
        v = Categorical(choices)
        for _ in range(50):
            assert v.sample({}) in choices

    def test_filter(self):
        v = Categorical(["a", "b", "c"])
        result = v.filter(["a", "x", "b", "y"], {})
        assert set(result) == {"a", "b"}

    def test_filter_empty_candidates(self):
        v = Categorical(["a", "b"])
        assert v.filter([], {}) == []

    def test_neighbor_different_from_value(self):
        v = Categorical(["a", "b", "c"])
        for _ in range(30):
            nb = v.neighbor("a", {})
            assert nb in {"b", "c"}

    def test_neighbor_single_choice(self):
        v = Categorical(["only"])
        assert v.neighbor("only", {}) == "only"

    def test_empty_choices_raises(self):
        with pytest.raises(ValueError):
            Categorical([])
