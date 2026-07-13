"""Kernel helpers for capacity-gap-roadmap. See SKILL.md."""

LEVERAGE_COLORS = {"High": "#1a7a3c", "Med": "#c98a00", "Low": "#999999"}
COST_COLORS = {"Low": "#1a7a3c", "Med": "#c98a00", "High": "#b2182b"}
POSTURE_COLORS = {
    "Amplify": "#0b4f8a",
    "Revive": "#5c2d91",
    "Connect": "#0b7a6f",
    "Build-via-partner": "#8a5a00",
    "Sustain": "#555555",
}

STAGE_ORDER = [
    "Disease understanding", "Diagnosis", "Research infrastructure",
    "Therapeutic development", "Regulatory", "Access", "Lived experience",
]


def style_or_default():
    """Apply figure-style if loaded; otherwise set safe defaults."""
    import matplotlib as mpl
    try:
        apply_figure_style()
    except Exception:
        mpl.rcParams.update({"font.family": "sans-serif", "figure.dpi": 200,
                             "savefig.dpi": 300, "savefig.bbox": "tight"})


def gap_map_from_inventory(gap_csv, leverage_map, active_map,
                           stage_col="pathway_stage",
                           sev_col="severity_1to5"):
    """Compute per-stage rows for render_gap_map from a gap_inventory.csv.

    leverage_map / active_map are dicts keyed by the stage label as it appears
    in the CSV (leading numbers are stripped for matching).
    Returns the `stages` list render_gap_map wants.
    """
    import pandas as pd
    df = pd.read_csv(gap_csv)

    def clean(s):
        s = str(s).strip()
        parts = s.split(None, 1)
        if parts and parts[0].rstrip(".").isdigit():
            s = parts[1] if len(parts) > 1 else s
        return s.strip()

    df["_stage"] = df[stage_col].apply(clean)
    rows = []
    for stage, grp in df.groupby("_stage", sort=False):
        rows.append({
            "stage": stage,
            "mean_severity": float(grp[sev_col].mean()),
            "n_gaps": int(len(grp)),
            "leverage": leverage_map.get(stage, "Med"),
            "org_active": bool(active_map.get(stage, False)),
        })
    return rows


def render_gap_map(stages, out_path="fig_gap_map.png", title=None,
                   subtitle=None, figsize=(11.8, 5.7)):
    """Render the patient-journey gap map.

    stages: list of {stage, mean_severity, n_gaps, leverage, org_active}.
    Bar height = mean severity; color = how directly the org can act;
    'already active' annotation marks stages with an existing footprint.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    style_or_default()
    try:
        grey = META_GREY
    except NameError:
        grey = "#888888"

    labels, sev, ng, lev, active = [], [], [], [], []
    for s in stages:
        lab = s["stage"]
        labels.append(lab.replace(" ", "\n", 1) if len(lab) > 12 else lab)
        sev.append(float(s["mean_severity"]))
        ng.append(int(s["n_gaps"]))
        lev.append(s.get("leverage", "Med"))
        active.append(bool(s.get("org_active", False)))

    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(labels))
    ax.bar(x, sev, width=0.62, color=[LEVERAGE_COLORS.get(l, "#999") for l in lev],
           edgecolor="#333", linewidth=0.6, zorder=3)
    ax.set_ylim(0, 5.8); ax.set_ylabel("Mean gap severity (1\u20135)")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7.6)
    ax.set_yticks([1, 2, 3, 4, 5]); ax.margins(x=0.02)
    for xi, (n, sv, act) in enumerate(zip(ng, sev, active)):
        ax.text(xi, sv + 0.12, "%.1f" % sv, ha="center", va="bottom",
                fontsize=7.5, fontweight="bold")
        ax.text(xi, 0.16, "%d gaps" % n, ha="center", va="bottom",
                fontsize=6.6, color="white", fontweight="bold")
        if act:
            ax.text(xi, sv + 0.42, "already\nactive here", ha="center",
                    va="bottom", fontsize=5.7, color="#0b4f8a", style="italic")
    present = [k for k in ["High", "Med", "Low"] if k in set(lev)]
    ax.legend(handles=[Patch(facecolor=LEVERAGE_COLORS[k], edgecolor="#333",
                             label="Org leverage: %s" % k) for k in present],
              loc="upper right", frameon=False, fontsize=7.5)
    if title:
        ax.set_title(title, fontsize=10, loc="left")
    if subtitle:
        ax.text(0.0, -0.31, subtitle, transform=ax.transAxes, fontsize=6.7,
                color=grey, va="top")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    return out_path


def render_roadmap(horizons, cards, backbone=None, out_path="fig_roadmap.png",
                   title=None, figsize=(13.2, 6.6)):
    """Render the phased capacity-building roadmap.

    horizons: list of (title, subtitle), one per column.
    cards:    dict {horizon_index: [(id, label, cost, posture), ...]}.
    backbone: optional dict {horizon_index: caption} for the bottom band.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Patch
    style_or_default()

    ncol = len(horizons)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, ncol); ax.set_ylim(1.7, 10.3); ax.axis("off")
    colw = 1.0
    if title:
        ax.text(0.0, 10.22, title, fontsize=9.6, fontweight="bold", va="top")

    for ci, (htitle, hsub) in enumerate(horizons):
        x0 = ci * colw
        ax.add_patch(FancyBboxPatch((x0 + 0.04, 9.05), colw - 0.08, 0.6,
                     boxstyle="round,pad=0.01,rounding_size=0.04",
                     facecolor="#10243a", edgecolor="none"))
        ax.text(x0 + colw / 2, 9.46, htitle, ha="center", va="center",
                color="white", fontsize=8.4, fontweight="bold")
        ax.text(x0 + colw / 2, 9.19, hsub, ha="center", va="center",
                color="#cdd8e4", fontsize=6.7, style="italic")
        cds = cards.get(ci, [])
        top = 8.7; ch = 0.78; gap = 0.135
        for i, card in enumerate(cds):
            rid, lab, cost, pos = card
            y = top - i * (ch + gap) - ch
            cc = COST_COLORS.get(cost, "#999")
            ax.add_patch(FancyBboxPatch((x0 + 0.06, y), colw - 0.12, ch,
                         boxstyle="round,pad=0.008,rounding_size=0.025",
                         facecolor="white", edgecolor=cc, linewidth=1.9))
            ax.text(x0 + 0.12, y + ch - 0.16, rid, fontsize=6.4,
                    fontweight="bold", color=cc, va="top")
            ax.text(x0 + 0.30, y + ch - 0.15, pos, fontsize=5.4, va="top",
                    color="white", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.15",
                              facecolor=POSTURE_COLORS.get(pos, "#555"),
                              edgecolor="none"))
            ax.text(x0 + 0.12, y + ch - 0.40, lab, fontsize=6.7, va="top")
            ax.text(x0 + colw - 0.09, y + 0.10, "%s cost" % cost, fontsize=5.7,
                    ha="right", color=cc, fontweight="bold")

    if backbone:
        ax.add_patch(FancyBboxPatch((0.04, 1.95), ncol - 0.08, 0.82,
                     boxstyle="round,pad=0.01,rounding_size=0.03",
                     facecolor="#eef3f8", edgecolor="#0b4f8a", linewidth=1.4))
        ax.text(ncol / 2, 2.58,
                "CAPACITY-BUILDING BACKBONE  (runs through every horizon)",
                ha="center", fontsize=7.4, color="#0b4f8a", fontweight="bold")
        for ci, cap in backbone.items():
            ax.text(ci * colw + colw / 2, 2.18, cap, ha="center", va="center",
                    fontsize=6.3, color="#0b4f8a")

    postures = []
    for cds in cards.values():
        for card in cds:
            if card[3] not in postures:
                postures.append(card[3])
    handles = [Patch(facecolor=COST_COLORS[k], edgecolor="#333",
                     label="%s cost/effort" % k)
               for k in ["Low", "Med", "High"]]
    handles += [Patch(facecolor=POSTURE_COLORS.get(p, "#555"), edgecolor="none",
                      label=p) for p in postures]
    ax.set_ylim(1.15, 10.3)
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.04),
              ncol=min(len(handles), 7), frameon=False, fontsize=6.6)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    return out_path
