"""Module for detecting stagnation."""
import logging
from typing import Dict, Any

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def detect_stagnation(df: pd.DataFrame, min_days: int = 28, min_sessions: int = 2) -> pd.DataFrame:
    logger.info(f"Detecting stagnation (min_days={min_days})")
    df = df.sort_values(["child_id", "domain", "session_date"])
    stagnation_cases = []
    for (child, domain), group in df.groupby(["child_id", "domain"]):
        group = group.reset_index(drop=True)
        stagnant_start = None
        stagnant_count = 0
        for i, row in group.iterrows():
            flag = str(row.get("progress_flag", "")).lower()
            is_stagnant = flag in ["stagnant", ""]
            if i > 0 and row["assessment_score"] == group.iloc[i-1]["assessment_score"]:
                is_stagnant = True
            if is_stagnant:
                if stagnant_start is None:
                    stagnant_start = i
                stagnant_count += 1
            else:
                if stagnant_start is not None and stagnant_count >= min_sessions:
                    start_date = group.iloc[stagnant_start]["session_date"]
                    end_date = group.iloc[i-1]["session_date"]
                    days = (end_date - start_date).days
                    if days >= min_days:
                        stagnation_cases.append(_build_case(child, domain, group, stagnant_start, i-1, days))
                stagnant_start = None
                stagnant_count = 0
        if stagnant_start is not None and stagnant_count >= min_sessions:
            start_date = group.iloc[stagnant_start]["session_date"]
            end_date = group.iloc[-1]["session_date"]
            days = (end_date - start_date).days
            if days >= min_days:
                stagnation_cases.append(_build_case(child, domain, group, stagnant_start, len(group)-1, days))
    if not stagnation_cases:
        return pd.DataFrame()
    result = pd.DataFrame(stagnation_cases)
    logger.info(f"Found {len(result)} cases")
    return result.sort_values("risk_level", ascending=False)


def _build_case(child_id, domain, group, start_idx, end_idx, days):
    start_date = group.iloc[start_idx]["session_date"]
    end_date = group.iloc[end_idx]["session_date"]
    if days > 90:
        risk = "critical"
    elif days > 60:
        risk = "high"
    elif days > 30:
        risk = "medium"
    else:
        risk = "low"
    return {
        "child_id": child_id, "domain": domain,
        "diagnosis": group.iloc[0].get("diagnosis", ""),
        "age": group.iloc[0].get("age", ""),
        "start_date": start_date, "end_date": end_date,
        "days_stagnant": days,
        "stagnant_sessions": end_idx - start_idx + 1,
        "last_score": group.iloc[end_idx]["assessment_score"],
        "risk_level": risk,
    }
