import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "child_id": ["SP01","SP01","SP01","SP02","SP02"],
        "domain": ["A","A","A","B","B"],
        "session_date": pd.to_datetime(["2026-01-01","2026-02-01","2026-03-15","2026-01-01","2026-03-01"]),
        "assessment_score": [3,3,3,5,5],
        "progress_flag": ["baseline","stagnant","stagnant","baseline","stagnant"],
        "diagnosis": ["RAS"]*5,
        "age": [4]*5,
        "comment": [""]*5,
        "specialist_type": ["logoped"]*5,
    })
