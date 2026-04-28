#!/usr/bin/env python3
import sys, logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from src.parser import load_sessions, prepare_analysis_data
from src.analysis import detect_stagnation
from src.reporting import save_stagnation_report, plot_child_dynamics, plot_summary_dashboard, generate_summary_md

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    p = Path("data/children_sessions.xlsx")
    if not p.exists():
        logger.error("No data file")
        sys.exit(1)
    logger.info("Loading...")
    df = load_sessions(str(p))
    df = prepare_analysis_data(df)
    logger.info("Detecting stagnation...")
    st = detect_stagnation(df, min_days=28)
    if not st.empty:
        print("\n=== STAGNATION CASES ===")
        print(st[["child_id","domain","days_stagnant","risk_level"]].to_string(index=False))
    logger.info("Saving...")
    save_stagnation_report(st, "outputs/stagnation_report.csv")
    generate_summary_md(st, df, "outputs/summary.md")
    plot_summary_dashboard(df, st, "outputs/plots")
    if not st.empty:
        for _, r in st[st["risk_level"].isin(["critical","high"])].iterrows():
            plot_child_dynamics(df, r["child_id"], f"outputs/plots/{r["child_id"]}_{r["domain"]}.png")
    logger.info("Done!")

if __name__ == "__main__":
    main()
