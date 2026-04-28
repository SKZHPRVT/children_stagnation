"""Tests for analysis."""
import pytest
import pandas as pd
from src.analysis import detect_stagnation


class TestDetectStagnation:
    def test_finds_stagnation(self, sample_df):
        result = detect_stagnation(sample_df, min_days=28)
        assert len(result) >= 1

    def test_min_days_filter(self, sample_df):
        result = detect_stagnation(sample_df, min_days=100)
        assert len(result) == 0

    def test_output_columns(self, sample_df):
        result = detect_stagnation(sample_df, min_days=28)
        for col in ["child_id","domain","days_stagnant","risk_level"]:
            assert col in result.columns
