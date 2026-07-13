"""Kernel helpers for disease-landscape-timeline. See SKILL.md."""

TRACK_COLORS = {
    "science": "#4C78A8",
    "regulatory": "#E45756",
    "natural history": "#72B7B2",
    "pipeline": "#F58518",
    "patient voice": "#9D4EDD",
}

TRACK_DISPLAY = {
    "science": "Science",
    "regulatory": "Regulatory",
    "natural history": "Natural history",
    "pipeline": "Pipeline",
    "patient voice": "Patient voice",
}

CSV_HEADER = "year,label,detail,category,confirmed\n"


def blank_milestones_csv(path="milestones.csv"):
    """Write an empty template CSV with the correct header."""
    with open(path, "w") as fh:
        fh.write(CSV_HEADER)
    return path


def norm_category(cat):
    key = str(cat).strip().lower()
    aliases = {
        "infrastructure": "natural history",
        "research infrastructure": "natural history",
        "registry": "natural history",
        "clinical": "pipeline",
        "trial": "pipeline",
        "pfdd": "patient voice",
        "approval": "regulatory",
    }
    return aliases.get(key, key)


def render_timeline(csv_path, out_path="research_timeline.png", title=None,
                    subtitle=None, figsize=(15, 7)):
    """Render a publication-grade disease-landscape timeline from a milestones CSV.

    CSV columns: year, label, detail (optional), category, confirmed (optional).
    category is matched case-insensitively to the five tracks (see TRACK_COLORS).
    Returns out_path.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib.patches import Patch

    try:
        apply_figure_style()  # from figure-style kernel if loaded
    except Exception:
        mpl.rcParams.update({"font.family": "sans-serif", "figure.dpi": 200,
                             "savefig.dpi": 300, "savefig.bbox": "tight"})

    df = pd.read_csv(csv_path)
    if "year" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV needs at least 'year' and 'label' columns")
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(float)
    df = df.sort_values("year").reset_index(drop=True)
    df["cat_norm"] = df.get("category", "science").apply(norm_category)

    # Stagger labels above/below; use up to 3 levels each side, scaled to density.
    n = len(df)
    n_levels = 3 if n > 6 else 2
    levels_up = [1.0 + i for i in range(n_levels)]
    levels_dn = [-(1.0 + i) for i in range(n_levels)]
    up_i = dn_i = 0
    placements = []
    for i in range(n):
        if i % 2 == 0:
            placements.append(levels_up[up_i % n_levels]); up_i += 1
        else:
            placements.append(levels_dn[dn_i % n_levels]); dn_i += 1

    ymax = n_levels + 0.9
    fig, ax = plt.subplots(figsize=figsize)
    ax.axhline(0, color="#bbb", lw=1, zorder=1)

    for i, row in df.iterrows():
        y = row["year"]; h = placements[i]
        col = TRACK_COLORS.get(row["cat_norm"], "#888888")
        ax.plot([y, y], [0, h * 0.9], color=col, lw=1.0, zorder=2, alpha=0.65)
        ax.scatter([y], [0], s=48, color=col, edgecolor="black", zorder=4)
        va = "bottom" if h > 0 else "top"
        yr_txt = str(int(row["year"])) if float(row["year"]).is_integer() else str(row["year"])
        ax.annotate("%s  %s" % (yr_txt, row["label"]), (y, h * 0.92),
                    fontsize=6.4, ha="center", va=va, color="black",
                    bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=col,
                              lw=0.8, alpha=0.97))

    # Ring the first regulatory approval and the latest patient-voice event.
    reg = df[df["cat_norm"] == "regulatory"]
    if len(reg):
        ax.scatter([reg.iloc[0]["year"]], [0], s=150, facecolor="none",
                   edgecolor=TRACK_COLORS["regulatory"], lw=1.8, zorder=5)
    pv = df[df["cat_norm"] == "patient voice"]
    if len(pv):
        ax.scatter([pv.iloc[-1]["year"]], [0], s=150, facecolor="none",
                   edgecolor=TRACK_COLORS["patient voice"], lw=1.8, zorder=5)

    span = df["year"].max() - df["year"].min()
    pad = max(2.0, span * 0.06)
    ax.set_xlim(df["year"].min() - pad, df["year"].max() + pad)
    ax.set_ylim(-ymax, ymax)
    ax.set_yticks([])
    ax.set_xlabel("Year")
    if title:
        ax.set_title(title, fontsize=10, loc="left", weight="bold")
    if subtitle:
        ax.text(0.0, 1.04, subtitle, transform=ax.transAxes, fontsize=7.5,
                color="#555")

    present = [c for c in TRACK_COLORS if c in set(df["cat_norm"])]
    ax.legend(handles=[Patch(facecolor=TRACK_COLORS[c], edgecolor="black",
                             label=TRACK_DISPLAY[c]) for c in present],
              loc="lower center", bbox_to_anchor=(0.5, -0.16),
              ncol=len(present), frameon=False, fontsize=7.5)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    return out_path
