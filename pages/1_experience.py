import streamlit as st
import pandas as pd
import plotly.express as px
from wc_ui import apply_theme, render_divider, render_metric_row, render_page_header, render_plot, render_section, style_plotly, render_data_source

### SETUP ###
st.set_page_config(
    page_title="The Weight of Experience",
    page_icon="1️⃣",
    layout="wide"
)
apply_theme()

last_wc = pd.read_csv("data/processed/winners.csv")
last_wc_nr = last_wc.nlargest(1, "year")["year"].iloc[0]

render_page_header(
    "The Weight of Experience",
    "Youth makes you run faster, but experience wins World Cups. Champion teams build their success on veteran backbones, especially in defensive positions.",
    eyebrow=f"World Cup Analytics (1930 - {last_wc_nr})"
)


### Data Import ###
# Wrap in try-except in case files are missing during preview
try:
    df_players_avg_age = pd.read_csv("data/processed/players_avg_age.csv")
    df_players = pd.read_csv("data/processed/players.csv")
    df_standings = pd.read_csv("data/processed/standings.csv")
    df_winners = pd.read_csv("data/processed/winners.csv")
except FileNotFoundError:
    st.error("Data files not found. Please ensure they are located in 'data/processed/'")
    st.stop()


# Merge Players Avg Age and Team Standings
df_age_stage = pd.merge(df_players_avg_age, df_standings, on=["year", "team"])
df_avg_age = (
    df_age_stage[
        ["year", "team", "avg_age", "stage_score", "final_position"]
    ]
    .drop_duplicates(subset=["year", "team"])
)

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
# Finalists Average Age
final_avg_age_df = df_age_stage[df_age_stage["final_position"]=="Final"]
final_avg_age = round(final_avg_age_df["avg_age"].mean(), 1) if not final_avg_age_df.empty else "N/A"

# Group Stage Exit Avg. Age
group_avg_age_df = df_age_stage[df_age_stage["final_position"]=="Group Stage"]
group_avg_age = round(group_avg_age_df["avg_age"].mean(), 1) if not group_avg_age_df.empty else "N/A"

# Oldest and Youngest Champions
df_finalists = df_age_stage[df_age_stage["final_position"].isin(["Final"])]
df_winners_age = df_winners.merge(df_finalists, on=["year","team"])
df_winners_age = df_winners_age[["year","team","position_x", "avg_age"]]
champions = df_winners_age[df_winners_age["position_x"] == 1]
youngest = champions.loc[champions["avg_age"].idxmin()]
oldest = champions.loc[champions["avg_age"].idxmax()]

# Render KPIs
render_metric_row([
    {"label": "Finalists Avg Age", "value": final_avg_age},
    {"label": "Group Stage Exit Avg Age", "value": group_avg_age},
    {"label": "Youngest Champion", "value": f"{youngest['team']} {youngest['year']}", "delta": f" {youngest['avg_age']:.0f} years", "delta_color": "off"},
    {"label": "Oldest Champion", "value": f"{oldest['team']} {oldest['year']}", "delta": f" {oldest['avg_age']:.0f} years", "delta_color": "off"},
])

render_divider()



#### Charts ###
order = (
    df_avg_age[["final_position", "stage_score"]]
    .drop_duplicates()
    .sort_values("stage_score")
    ["final_position"]
    .tolist()
)

col_left, col_right = st.columns([0.6, 0.4])

# Swarm plot avg_age x final_position
with col_left:
    fig = px.strip(
        df_avg_age, 
        x="final_position", 
        y="avg_age", 
        stripmode="group", 
        hover_data=["team", "year"], 
        labels={"final_position": "Tournament stage", "avg_age": "Average squad age", "team": "Team", "year": "World Cup"},
        category_orders={"final_position": order}
    )
    fig = style_plotly(fig)
    render_section("Average Squad Age by Tournament Stage")
    render_plot(fig, theme="streamlit")


# Box plot avg_age x final_position
with col_right:
    fig = px.box(
        df_avg_age, x="final_position", y="avg_age", 
        labels={"final_position": "Tournament stage", "avg_age": "Average squad age"},
        category_orders={"final_position": order}
    )
    fig = style_plotly(fig)
    render_section("Age Distribution of Squads (Quartiles)")
    render_plot(fig, theme="streamlit")

st.success("💡 **Insight:** While average age changes little across tournament stages, finalists are concentrated around the middle of the age distribution rather than its extremes.")

render_divider()

# 2. MACRO: TACTICAL HEATMAP
render_section("Tactical Age Heatmap", "Average age distribution by tactical position and tournament stage reached.")

# Create the matrix using pivot_table
heatmap_data = df_age_stage.pivot_table(
    index='position',           # Rows: Tactical positions
    columns='final_position',   # Columns: Stages reached
    values='avg_age_p_pos',     # Heatmap cell values: Average age
    aggfunc='mean'              # Aggregate by taking the mean
)

position_order = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
stage_order = [
    'Group Stage', 
    'Round of 16', 
    'Quarterfinals', 
    'Semifinals', 
    'Final', 
    'Champion'
]

# Apply the logical sorting, keeping only columns/rows that exist
existing_positions = [p for p in position_order if p in heatmap_data.index]
existing_stages = [s for s in stage_order if s in heatmap_data.columns]
heatmap_data = heatmap_data.loc[existing_positions, existing_stages]

# Render the Heatmap with Plotly Express
fig_heatmap = px.imshow(
    heatmap_data,
    labels=dict(
        x="Tournament stage", 
        y="Tactical position", 
        color="Average age"
    ),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    text_auto='.1f',
    aspect="auto",
    color_continuous_scale='Cividis',
    origin='upper'
)

fig_heatmap = style_plotly(
    fig_heatmap,
    margin=dict(l=0, r=0, t=30, b=0)
)

fig_heatmap.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    plot_bgcolor='rgba(0,0,0,0)'
)

render_plot(fig_heatmap, theme="streamlit")

st.success("💡 **Insight:** Goalkeepers are consistently the oldest players, while forwards are the youngest. Teams reaching the final also tend to have slightly older players across every tactical position.")

render_divider()


# 3. MICRO / EXPLORATORY: SQUAD AGE PROFILE
render_section("Squad Age Profile vs Tournament Average", "Analyze a specific team's age curve against the rest of the competition for that year.")

# Selectors in smaller columns
col_sel1, col_sel2, _ = st.columns([2, 2, 6])
with col_sel1:
    year_selected = st.selectbox("Select Year", sorted(df_players["year"].unique(), reverse=True))
with col_sel2:
    available_teams = sorted(df_players[df_players["year"] == year_selected]["team"].unique())
    # Default to Argentina if available, otherwise first in list
    default_index = available_teams.index("Argentina") if "Argentina" in available_teams else 0
    team_selected = st.selectbox("Select Team", available_teams, index=default_index)

# Prepare Histogram Data
df_hist = df_players[["year", "team", "age"]].copy()
df_hist["group"] = "All Players"

df_team = df_hist[
    (df_hist["team"] == team_selected) & 
    (df_hist["year"] == year_selected)
].copy()
df_team["group"] = f"{team_selected} {year_selected}"

df_plot = pd.concat([
    df_hist[df_hist["year"] == year_selected], # Compare against players from the SAME tournament
    df_team
])

# Create the overlapping histogram
fig_hist = px.histogram(
    df_plot,
    x="age",
    color="group",
    barmode="overlay",
    histnorm="probability density",
    opacity=0.6,
    color_discrete_map={
        "All Players": "#64748b",
        f"{team_selected} {year_selected}": "#7dd3fc"
    },
    labels={"age": "Player age", "group": "Cohort"}
)

fig_hist = style_plotly(
    fig_hist,
    margin=dict(l=0, r=0, t=30, b=0)
)

fig_hist.update_layout(
    yaxis_title="Density",
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
)

render_plot(fig_hist)


render_data_source()