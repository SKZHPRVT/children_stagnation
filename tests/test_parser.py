"""Tests for parser."""
import pytest
import pandas as pd
from src.parser import _fill_progress_flags


class TestFillProgressFlags:
    def test_fills_missing_flags(self):
        df = pd.DataFrame({
            "child_id": ["SP01","SP01","SP01"],
            "domain": ["A","A","A"],
            "session_date": pd.to_datetime(["2026-01-01","2026-02-01","2026-03-01"]),
            "assessment_score": [3,5,5],
            "progress_flag": ["","",""],
            "diagnosis": ["RAS"]*3,
            "age": [4]*3,
            "comment": [""]*3,
            "specialist_type": ["logoped"]*3,
        })
        result = _fill_progress_flags(df)
        assert result.iloc[0]["progress_flag"] == "baseline"
        assert result.iloc[1]["progress_flag"] == "improved"
        assert result.iloc[2]["progress_flag"] == "stagnant"
