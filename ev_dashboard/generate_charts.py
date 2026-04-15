# =============================================
#   EVPULSE DASHBOARD — generate_charts.py
#   Path: ev_dashboard/generate_charts.py
#
#   It will generate these 7 charts and save then in the 'charts' folder.
#   1. top_makes.png          — Top 10 EV Brands (Bar)
#   2. ev_type_pie.png        — BEV vs PHEV (Pie)
#   3. model_year_trend.png   — Year-wise Growth (Line)
#   4. range_distribution.png — Electric Range (Histogram)
#   5. top_cities.png         — Top 15 Cities (Horizontal Bar)
#   6. cafv_eligibility.png   — CAFV Eligibility (Donut)
#   7. make_year_heatmap.png  — Make x Year (Heatmap)
# =============================================

import os
import warnings
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---- Warnings band karo ----
warnings.filterwarnings("ignore")
matplotlib.use("Agg")   # GUI window na kholo — file mein save karo

# ============================================================
#   PATHS
# ============================================================
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_PATH  = os.path.join(BASE_DIR, "data", "Electric_Vehicle_Population_Data.csv")
CHART_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
#   DARK THEME — Sab charts ke liye common styling
# ============================================================
BG        = "#050a12"
SURFACE   = "#0d1627"
SURFACE2  = "#111e35"
ACCENT    = "#00c8ff"
ACCENT2   = "#00ff9d"
ACCENT3   = "#ff4d6d"
TEXT      = "#e8f4ff"
TEXT_SUB  = "#6b8cae"
GRID_COL  = "#1a2d45"

# Matplotlib global style set karo
plt.rcParams.update({
    "figure.facecolor"  : BG,
    "axes.facecolor"    : SURFACE,
    "axes.edgecolor"    : GRID_COL,
    "axes.labelcolor"   : TEXT_SUB,
    "axes.titlecolor"   : TEXT,
    "axes.titlesize"    : 14,
    "axes.titleweight"  : "bold",
    "axes.titlepad"     : 16,
    "axes.grid"         : True,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "grid.color"        : GRID_COL,
    "grid.linewidth"    : 0.6,
    "grid.alpha"        : 0.6,
    "xtick.color"       : TEXT_SUB,
    "ytick.color"       : TEXT_SUB,
    "xtick.labelsize"   : 9,
    "ytick.labelsize"   : 9,
    "text.color"        : TEXT,
    "font.family"       : "DejaVu Sans",
    "legend.facecolor"  : SURFACE2,
    "legend.edgecolor"  : GRID_COL,
    "legend.labelcolor" : TEXT,
    "savefig.facecolor" : BG,
    "savefig.bbox"      : "tight",
    "savefig.dpi"       : 150,
})

# Color palette — gradient style
PALETTE = [ACCENT, ACCENT2, ACCENT3,
           "#7b61ff", "#ffb830", "#ff6b9d",
           "#00e5cc", "#4fc3f7", "#aed581", "#ffd54f"]


# ============================================================
#   CSV LOAD
# ============================================================
def load_data():
    print(f"\n📂 CSV load ho raha hai: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"❌ CSV nahi mila!\n"
            f"   '{CSV_PATH}' mein file daalo."
        )
    df = pd.read_csv(CSV_PATH)
    print(f"✅ {len(df):,} rows load hui")
    return df


# ============================================================
#   HELPER — Chart Save Karna
# ============================================================
def save_chart(fig, name):
    path = os.path.join(CHART_DIR, name)
    fig.savefig(path)
    # plt.show()
    plt.close(fig)
    print(f"   💾 Saved → charts/{name}")


# ============================================================
#   CHART 1 — Top 10 EV Manufacturers (Horizontal Bar)
# ============================================================
def chart_top_makes(df):
    print("\n📊 Chart 1: Top 10 EV Makes...")

    top = df["Make"].value_counts().head(10).sort_values()
    colors = [ACCENT if m == "TESLA" else SURFACE2 for m in top.index]
    bar_colors = []
    for i, m in enumerate(top.index):
        if m == "TESLA":
            bar_colors.append(ACCENT)
        else:
            bar_colors.append(PALETTE[i % len(PALETTE)])

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top.index, top.values, color=bar_colors,
                   edgecolor="none", height=0.65)

    # Value labels
    for bar, val in zip(bars, top.values):
        ax.text(val + 500, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", ha="left",
                fontsize=9, color=TEXT_SUB)

    ax.set_title("Top 10 EV Manufacturers")
    ax.set_xlabel("Number of Vehicles")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
    ax.set_xlim(0, top.values.max() * 1.18)
    ax.tick_params(axis="y", labelsize=10)

    # Tesla highlight annotation
    tesla_val = top.get("TESLA", None)
    if tesla_val:
        ax.annotate("⚡ Market Leader",
                    xy=(tesla_val, top.index.tolist().index("TESLA")),
                    xytext=(tesla_val * 0.6, top.index.tolist().index("TESLA") + 0.5),
                    color=ACCENT, fontsize=8,
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))

    fig.tight_layout(pad=2)
    save_chart(fig, "top_makes.png")


# ============================================================
#   CHART 2 — BEV vs PHEV Pie Chart
# ============================================================
def chart_ev_type_pie(df):
    print("\n📊 Chart 2: BEV vs PHEV Pie...")

    counts = df["Electric Vehicle Type"].value_counts()
    labels = ["Battery Electric\n(BEV)", "Plug-in Hybrid\n(PHEV)"]
    sizes  = [counts.get("Battery Electric Vehicle (BEV)", 0),
              counts.get("Plug-in Hybrid Electric Vehicle (PHEV)", 0)]
    colors = [ACCENT, ACCENT3]
    explode = (0.04, 0.04)

    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct="%1.1f%%", startangle=120,
        pctdistance=0.75, labeldistance=1.12,
        wedgeprops=dict(edgecolor=BG, linewidth=2.5),
        textprops=dict(color=TEXT, fontsize=10)
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
        at.set_color(BG)

    ax.set_title("BEV vs PHEV Split")
    fig.tight_layout(pad=2)
    save_chart(fig, "ev_type_pie.png")


# ============================================================
#   CHART 3 — EV Adoption by Model Year (Line Chart)
# ============================================================
def chart_model_year_trend(df):
    print("\n📊 Chart 3: Model Year Trend...")

    df2   = df[df["Model Year"].notna()].copy()
    df2["Model Year"] = df2["Model Year"].astype(int)
    trend = df2["Model Year"].value_counts().sort_index()
    trend = trend[(trend.index >= 2010) & (trend.index <= 2025)]

    fig, ax = plt.subplots(figsize=(10, 5))

    # Area fill
    ax.fill_between(trend.index, trend.values,
                    alpha=0.15, color=ACCENT)
    ax.plot(trend.index, trend.values,
            color=ACCENT, linewidth=2.5, marker="o",
            markersize=6, markerfacecolor=ACCENT2,
            markeredgecolor=BG, markeredgewidth=1.5)

    # Peak annotation
    peak_year  = trend.idxmax()
    peak_count = trend.max()
    ax.annotate(f"Peak: {peak_year}\n{peak_count:,} EVs",
                xy=(peak_year, peak_count),
                xytext=(peak_year - 2, peak_count * 0.85),
                color=ACCENT2, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=ACCENT2, lw=1.2))

    ax.set_title("EV Adoption by Model Year (2010–2025)")
    ax.set_xlabel("Model Year")
    ax.set_ylabel("Number of Vehicles")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
    ax.set_xticks(trend.index)
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout(pad=2)
    save_chart(fig, "model_year_trend.png")


# ============================================================
#   CHART 4 — Electric Range Distribution (Histogram)
# ============================================================
def chart_range_distribution(df):
    print("\n📊 Chart 4: Electric Range Distribution...")

    ranges = df[df["Electric Range"] > 0]["Electric Range"].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    n, bins, patches = ax.hist(ranges, bins=35,
                                color=ACCENT, edgecolor=BG,
                                alpha=0.85, linewidth=0.8)

    # Color gradient effect
    max_n = max(n)
    for patch, val in zip(patches, n):
        intensity = val / max_n
        r = int(0   + intensity * 0)
        g = int(200 * intensity)
        b = int(255 * intensity)
        patch.set_facecolor(f"#{0:02x}{int(g):02x}{int(b):02x}")

    # Mean line
    mean_range = ranges.mean()
    ax.axvline(mean_range, color=ACCENT2, linestyle="--",
               linewidth=1.8, label=f"Average: {mean_range:.0f} miles")

    # Median line
    median_range = ranges.median()
    ax.axvline(median_range, color=ACCENT3, linestyle=":",
               linewidth=1.8, label=f"Median: {median_range:.0f} miles")

    ax.set_title("Electric Range Distribution")
    ax.set_xlabel("Electric Range (miles)")
    ax.set_ylabel("Number of Vehicles")
    ax.legend(loc="upper right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K"))

    fig.tight_layout(pad=2)
    save_chart(fig, "range_distribution.png")


# ============================================================
#   CHART 5 — Top 15 Cities by EV Count (Horizontal Bar)
# ============================================================
def chart_top_cities(df):
    print("\n📊 Chart 5: Top 15 Cities...")

    top = df["City"].value_counts().head(15).sort_values()

    # Color — darker to brighter
    cmap   = plt.cm.get_cmap("cool", len(top))
    colors = [cmap(i) for i in range(len(top))]

    fig, ax = plt.subplots(figsize=(11, 7))
    bars = ax.barh(top.index, top.values,
                   color=colors, edgecolor="none", height=0.65)

    for bar, val in zip(bars, top.values):
        ax.text(val + 100, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", ha="left",
                fontsize=8.5, color=TEXT_SUB)

    ax.set_title("Top 15 Cities by EV Count")
    ax.set_xlabel("Number of Vehicles")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
    ax.set_xlim(0, top.values.max() * 1.2)
    ax.tick_params(axis="y", labelsize=9)

    fig.tight_layout(pad=2)
    save_chart(fig, "top_cities.png")


# ============================================================
#   CHART 6 — CAFV Eligibility (Donut Chart)
# ============================================================
def chart_cafv_eligibility(df):
    print("\n📊 Chart 6: CAFV Eligibility Donut...")

    counts = df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].value_counts()

    # Short labels
    label_map = {
        "Clean Alternative Fuel Vehicle Eligible"                       : "Eligible ✅",
        "Eligibility unknown as battery range has not been researched"  : "Unknown ❓",
        "Not eligible due to low battery range"                         : "Not Eligible ❌",
        "Clean Alternative Fuel Vehicle Eligible (Partial)"             : "Partial ⚡",
    }
    labels = [label_map.get(k, k[:25]) for k in counts.index]
    colors = [ACCENT2, TEXT_SUB, ACCENT3, ACCENT][:len(counts)]

    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
        labeldistance=1.14,
        wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2.5),
        textprops=dict(color=TEXT, fontsize=9)
    )

    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
        at.set_color(BG)

    # Center text
    ax.text(0, 0, f"{counts.values.sum():,}\nTotal",
            ha="center", va="center",
            fontsize=12, fontweight="bold", color=TEXT)

    ax.set_title("CAFV Eligibility Breakdown")
    fig.tight_layout(pad=2)
    save_chart(fig, "cafv_eligibility.png")


# ============================================================
#   CHART 7 — Make × Model Year Heatmap
# ============================================================
def chart_make_year_heatmap(df):
    print("\n📊 Chart 7: Make × Year Heatmap...")

    df2 = df[df["Model Year"].notna()].copy()
    df2["Model Year"] = df2["Model Year"].astype(int)
    df2 = df2[(df2["Model Year"] >= 2015) & (df2["Model Year"] <= 2024)]

    # Top 10 makes
    top_makes = df2["Make"].value_counts().head(10).index.tolist()
    df2 = df2[df2["Make"].isin(top_makes)]

    pivot = df2.pivot_table(
        index="Make",
        columns="Model Year",
        values="VIN (1-10)",
        aggfunc="count",
        fill_value=0
    )
    # Sort by total
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(13, 6))

    sns.heatmap(
        pivot,
        ax=ax,
        cmap=sns.color_palette("mako", as_cmap=True),
        linewidths=0.4,
        linecolor=BG,
        annot=True,
        fmt=",",
        annot_kws={"size": 8, "color": TEXT},
        cbar_kws={"shrink": 0.7, "label": "Vehicle Count"}
    )

    # Colorbar style
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.label.set_color(TEXT_SUB)
    cbar.ax.tick_params(colors=TEXT_SUB)

    ax.set_title("EV Make × Model Year — Heatmap (2015–2024)")
    ax.set_xlabel("Model Year", labelpad=10)
    ax.set_ylabel("Make", labelpad=10)
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)

    fig.tight_layout(pad=2)
    save_chart(fig, "make_year_heatmap.png")


# ============================================================
#   MAIN — Sab Charts Ek Saath Generate Karo
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  ⚡ EVPULSE — Chart Generator Starting...")
    print("=" * 55)

    # Data load karo
    df = load_data()

    # Saare charts generate karo
    chart_top_makes(df)
    chart_ev_type_pie(df)
    chart_model_year_trend(df)
    chart_range_distribution(df)
    chart_top_cities(df)
    chart_cafv_eligibility(df)
    chart_make_year_heatmap(df)

    print("\n" + "=" * 55)
    print("  ✅ Saare 7 charts ban gaye!")
    print(f"  📁 Folder: {CHART_DIR}")
    print("=" * 55)
    print("\n  Charts list:")
    charts = [
        "top_makes.png          — Top 10 EV Brands",
        "ev_type_pie.png        — BEV vs PHEV Pie",
        "model_year_trend.png   — Year-wise Growth",
        "range_distribution.png — Range Histogram",
        "top_cities.png         — Top 15 Cities",
        "cafv_eligibility.png   — CAFV Donut",
        "make_year_heatmap.png  — Make x Year Heatmap",
    ]
    for c in charts:
        print(f"  ✔  {c}")

    print("\n  🌐 Ab 'python app.py' chalao aur browser mein")
    print("     http://localhost:5000 kholo!\n")


# Line no 29 & 111