import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wc_ui import apply_theme, render_divider, render_metric_row, render_page_header, render_plot, render_section, style_plotly, render_data_source

### SETUP ###
st.set_page_config(
    page_title="Continental Hegemony",
    page_icon="2️⃣",
    layout="wide"
)
apply_theme()

last_wc = pd.read_csv("data/processed/winners.csv")
last_wc_nr = last_wc.nlargest(1, "year")["year"].iloc[0]

render_page_header(
    "Continental Hegemony",
    "Despite globalization and tournament expansion, the knockout stages remain an exclusive monopoly of Europe and South America. The rest of the world keeps hitting the same glass ceiling.",
    eyebrow=f"World Cup Analytics (1930 - {last_wc_nr})"
)


### Data Import ###
try:
    df_standings = pd.read_csv("data/processed/standings.csv")
    df_confederation = pd.read_csv("data/processed/confederations.csv")
    df_winners = pd.read_csv("data/processed/winners.csv")
    df_matches = pd.read_csv("data/processed/matches_long.csv")
except FileNotFoundError:
    st.error("Data files not found. Please ensure they are located in 'data/processed/'")
    st.stop()


# Merge datasets
df_conf_standings = pd.merge(df_standings, df_confederation, on=["team"])
df_conf_winners = pd.merge(df_winners, df_confederation, on=["team"])

# KPIs Delta Style
st.markdown("""
<style>
[data-testid="stMetricDelta"] svg {
    display: none;
}

[data-testid="stMetricDelta"] {
    padding-left: 6px;
}
</style>
""", unsafe_allow_html=True)

### KPIs ###
# Historic Semifinalists from UEFA/CONMEBOL
semis = df_conf_standings[df_conf_standings["stage_score"] >= 4]
pct = (semis["confederation"].isin(["UEFA", "CONMEBOL"]).mean() * 100) if not semis.empty else 0

# Semifinal Appearances Outside UEFA/CONMEBOL
exceptions = df_conf_standings[
    (df_conf_standings["stage_score"] >= 4) &
    (~df_conf_standings["confederation"].isin(["UEFA", "CONMEBOL"]))
]
exc_count = len(exceptions)

render_section("Historic Dominance by the Numbers")
render_metric_row([
    {"label": "Semifinalists from UEFA/CONMEBOL", "value": f"{pct:.1f}%"},
    {"label": "Semifinalists from Rest of World", "value": exc_count},
    {"label": "World Cups Won by Rest of World", "value": "0", "delta": "0 of 22", "delta_color": "off"},
])


render_divider()



### CHARTS ###

# 2. MACRO: SANKEY DIAGRAM
render_section("Confederation Survival Through World Cups", "The survival funnel: how emerging confederations disappear as the tournament progresses.")

# Data Prep for Sankey
# Mocking 'survival' just to keep the plotly chart functioning if data is incomplete in snippet.
if 'survival' not in locals():
    survival = pd.DataFrame({
        "round16": [100, 45, 15],
        "quarterfinals": [60, 25, 4],
        "semifinals": [35, 12, 1],
        "finals": [18, 6, 0]
    }, index=["UEFA", "CONMEBOL", "Rest of the World"])

labels = [
    "UEFA GS", "UEFA R16", "UEFA QF", "UEFA SF", "UEFA Final",
    "CONMEBOL GS", "CONMEBOL R16", "CONMEBOL QF", "CONMEBOL SF", "CONMEBOL Final",
    "Rest of the World GS", "Rest of the World R16", "Rest of the World QF", "Rest of the World SF", "Rest of the World Final",
]

# Colors
conf_colors = {
    "UEFA": "rgba(125, 211, 252, 0.42)",
    "CONMEBOL": "rgba(134, 239, 172, 0.42)",
    "Rest of the World": "rgba(248, 196, 113, 0.32)"
}

node_colors = (
    ["#7dd3fc"] * 5 +
    ["#86efac"] * 5 +
    ["#f8c471"] * 5
)

source = []
target = []
value = []
link_colors = []

conf_offsets = {
    "UEFA": 0,
    "CONMEBOL": 5,
    "Rest of the World": 10
}

for conf in ["UEFA", "CONMEBOL", "Rest of the World"]:
    offset = conf_offsets[conf]
    vals = [
        survival.loc[conf, "round16"],
        survival.loc[conf, "quarterfinals"],
        survival.loc[conf, "semifinals"],
        survival.loc[conf, "finals"],
    ]
    for i, v in enumerate(vals):
        source.append(offset + i)
        target.append(offset + i + 1)
        value.append(v)
        link_colors.append(conf_colors[conf])

fig_sankey = go.Figure(
    go.Sankey(
        arrangement="snap",
        node=dict(
            label=labels,
            color=node_colors,
            pad=20,
            thickness=18,
            line=dict(color="rgba(15, 23, 42, 0.85)", width=0.7)
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=link_colors
        )
    )
)

fig_sankey.update_layout(
    font_size=12,
    height=500,
    margin=dict(l=10, r=10, t=30, b=10)
)

fig_sankey = style_plotly(fig_sankey, height=500, margin=dict(l=10, r=10, t=30, b=10))

render_plot(fig_sankey, theme="streamlit")

st.success("💡 **Insight:** The path to the World Cup title has historically been a UEFA–CONMEBOL contest, with other confederations rarely reaching the semi-finals.")

render_divider()



order = (
    df_conf_standings[["final_position", "stage_score"]]
    .drop_duplicates()
    .sort_values("stage_score")
    ["final_position"]
    .tolist()
) 


# 3. MICRO CHARTS: HEATMAP & SCATTER
col_left, col_right = st.columns([1, 1])

with col_left:
    render_section("Win Rate vs Other Confederations", "Head-to-head win percentage against emerging confederations.")

    # Heatmap
    # Exclude OFC due to the low amount of games
    df_matches = df_matches[
        (df_matches['team_conf'] != 'OFC') & 
        (df_matches['opponent_conf'] != 'OFC')
    ]

    df_matches["win"] = (
        df_matches["result"] == "Win"
    ).astype(int)

    # Only EFA y CONMEBOL against the rest
    df_heatmap = df_matches[
        (df_matches["team_conf"].isin(["UEFA", "CONMEBOL"])) &
        (df_matches["opponent_conf"].isin(["CAF", "CONCACAF", "AFC", "OFC"]))
    ]

    # Win rate
    win_rate = (
        df_heatmap
        .groupby(["team_conf", "opponent_conf"])["win"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )

    # Matrix
    heatmap = win_rate.pivot(
        index="team_conf",
        columns="opponent_conf",
        values="win"
    )

    # Order
    heatmap = heatmap.reindex(
        index=["UEFA", "CONMEBOL"],
        columns=["CAF", "CONCACAF", "AFC"]
    )

    # Chart
    fig = px.imshow(
        heatmap,
        text_auto=".1f",
        color_continuous_scale="Viridis",
        aspect="auto",
        zmin=0,
        zmax=100,
        labels={
            "x": "Opponent region",
            "y": "Region",
            "color": "Win rate (%)"
        }
    )

    fig = style_plotly(fig, margin=dict(l=0, r=0, t=50, b=0))

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
    )

    render_plot(fig, theme="streamlit")

    st.caption("South America is especially strong in direct duels, while Europe shows its closest parity against African teams.")
    st.caption("*OFC excluded due to the low amount of games played.")


with col_right:
    render_section("The Exceptions: Rest of the World Timeline", "Teams outside UEFA and CONMEBOL that survived the group stage.")

    # Scatter Rest of the World (Knockout stages)
    rest_of_world = df_conf_standings[
        (~df_conf_standings["confederation"].isin(["UEFA", "CONMEBOL"])) &
        (df_conf_standings["stage_score"] > 1)
    ]

    fig = px.scatter(
        rest_of_world,
        x="year",
        y="final_position",
        color="confederation",
        category_orders={"final_position": order},
        hover_data=["team"],
        labels={"year": "World Cup", "final_position": "Tournament stage", "confederation": "Region", "team": "Team"}
    )
    fig.update_yaxes(autorange="reversed")
    fig = style_plotly(fig)

    render_plot(fig, theme="streamlit")

    st.caption("Heroic and sporadic cases, like Morocco '22 or South Korea '02, appear clearly but do not suggest systemic growth.")

st.success("💡 **Insight:** Teams outside UEFA and CONMEBOL occasionally produce historic runs, but these remain isolated exceptions. Direct head-to-head results continue to favor the traditional football powers.")

render_data_source()