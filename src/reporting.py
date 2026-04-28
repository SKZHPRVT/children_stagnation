"""Module for reports and visualizations."""
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)
plt.style.use("seaborn-v0_8-darkgrid")


def save_stagnation_report(df, path):
    if df.empty:
        return
    df.to_csv(path, index=False)
    logger.info(f"Saved to {path}")


def plot_child_dynamics(df, child_id, path):
    data = df[df["child_id"] == child_id]
    if data.empty:
        return
    domains = data["domain"].unique()
    fig, axes = plt.subplots(len(domains), 1, figsize=(10, 3*len(domains)), squeeze=False)
    for i, d in enumerate(domains):
        ax = axes[i][0]
        dd = data[data["domain"] == d].sort_values("session_date")
        ax.plot(dd["session_date"], dd["assessment_score"], marker="o", linewidth=2, markersize=8)
        st = dd[dd["progress_flag"].isin(["stagnant", ""])]
        if not st.empty:
            ax.scatter(st["session_date"], st["assessment_score"], color="red", s=100, zorder=5, label="Stagnant")
        ax.set_title(f"{child_id} - {d}")
        ax.set_ylabel("Score")
        ax.grid(True, alpha=0.3)
        if not st.empty:
            ax.legend()
    plt.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_summary_dashboard(df, stagnation, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if not stagnation.empty:
        fig, ax = plt.subplots(figsize=(8,5))
        rc = stagnation["risk_level"].value_counts()
        colors = {"critical":"red","high":"orange","medium":"yellow","low":"green"}
        ax.bar(rc.index, rc.values, color=[colors.get(r,"gray") for r in rc.index])
        ax.set_title("Risk distribution")
        fig.savefig(out/"risk_distribution.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        fig, ax = plt.subplots(figsize=(8,5))
        dc = stagnation["domain"].value_counts()
        ax.barh(dc.index, dc.values)
        ax.set_title("Stagnation by domain")
        fig.savefig(out/"stagnation_by_domain.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(10,5))
    avg = df.groupby("child_id")["assessment_score"].mean().sort_values()
    ax.barh(avg.index, avg.values)
    ax.set_title("Average score by child")
    fig.savefig(out/"avg_score_by_child.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def generate_summary_md(stag, df, path):
    lines = []
    lines.append("# Stagnation Summary")
    lines.append("")
    lines.append(f"Children: {df["child_id"].nunique()}, Sessions: {len(df)}")
    if stag.empty:
        lines.append("No stagnation found.")
    else:
        lines.append(f"Cases: {len(stag)}")
        for risk in ["critical","high","medium","low"]:
            n = len(stag[stag["risk_level"]==risk])
            if n:
                lines.append(f"- {risk}: {n}")
    Path(path).write_text("\n".join(lines))
