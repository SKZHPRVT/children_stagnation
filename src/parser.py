"""Module for loading and preprocessing children session data."""
import logging
from typing import Dict, Any

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def load_sessions(filepath: str) -> pd.DataFrame:
    logger.info(f"Loading sessions from {filepath}")
    df = pd.read_excel(filepath)
    required = ["child_id", "domain", "session_date", "assessment_score"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["session_date"] = pd.to_datetime(df["session_date"], errors="coerce")
    df["assessment_score"] = pd.to_numeric(df["assessment_score"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df = _fill_progress_flags(df)
    logger.info(f"Loaded {len(df)} sessions")
    return df


def _fill_progress_flags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["child_id", "domain", "session_date"])
    for (child, domain), group in df.groupby(["child_id", "domain"]):
        scores = group["assessment_score"].values
        for i in range(len(group)):
            idx = group.index[i]
            flag = df.loc[idx, "progress_flag"] if "progress_flag" in df.columns else ""
            if pd.isna(flag) or str(flag).strip() == "":
                if i == 0:
                    df.loc[idx, "progress_flag"] = "baseline"
                elif scores[i] > scores[i-1]:
                    df.loc[idx, "progress_flag"] = "improved"
                elif scores[i] == scores[i-1]:
                    df.loc[idx, "progress_flag"] = "stagnant"
                else:
                    df.loc[idx, "progress_flag"] = "regressed"
    return df


def prepare_analysis_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["child_id", "domain", "session_date"])
    return df
