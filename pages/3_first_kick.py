import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wc_ui import apply_theme, render_divider, render_metric_row, render_page_header, render_plot, render_section, style_plotly, render_data_source


### SETUP ###
st.set_page_config(
    page_title="The First Kick Advantage",
    page_icon="3️⃣",
    layout="wide"
)
apply_theme()

last_wc = pd.read_csv("data/processed/winners.csv")
last_wc_nr = last_wc.nlargest(1, "year")["year"].iloc[0]

render_page_header(
    "The First Kick Advantage",
    "Historically, it is believed that taking the first kick in a penalty shootout gives a psychological advantage, resulting in a win rate over 60%.",
    eyebrow=f"World Cup Analytics (1930 - {last_wc_nr})"
)


### Data import ###
df_penalty = pd.read_csv("data/processed/penalty_shootouts.csv")



### KPIs ###
# First team to take penalty win rate (%)
# One row per shootout
shootouts = (
    df_penalty.groupby(["year", "round", "winner", "loser"])
      .first()
      .reset_index()
)

first_team = (
    df_penalty[df_penalty["first_taker"]]
    .groupby(["year", "round", "winner", "loser"])["team"]
    .first()
    .reset_index(name="first_team")
)

shootouts = shootouts.merge(
    first_team,
    on=["year", "round", "winner", "loser"]
)

shootouts["first_team_won"] = (
    shootouts["first_team"] == shootouts["winner"]
)

win_rate = shootouts["first_team_won"].mean() * 100


# Total penalty shootouts
n_shootouts = (
    df_penalty[["year", "round", "winner", "loser"]]
    .drop_duplicates()
    .shape[0]
)

# Penalties scored %
penalties_scored = (df_penalty[df_penalty["scored"]==True].shape[0] / df_penalty.shape[0])*100

# 2. THE KPIs
render_section("The Verdict")
render_metric_row([
    {"label": "1st Kicker Wins", "value": f"{win_rate:.1f}%", "delta": "-11% vs Myth", "delta_color": "inverse"},
    {"label": "2nd Kicker Wins", "value": f"{(100 - win_rate):.1f}%"},
    {"label": "Global Conversion", "value": f"{penalties_scored:.1f}%"},
])

render_divider()



### Charts ###
# MACRO CHART (Tornado Chart)
render_section("Penalty Conversion Decay by Round", "The anatomy of psychological pressure throughout the shootout.")

# 1. Cargar datos directamente (asegúrate de que el CSV esté en la misma carpeta que el Notebook)
df = df_penalty.copy()

# 2. Procesamiento: Identificar quién pateó primero en cada tanda
# Crear un ID único por partido
df['match_id'] = df['year'].astype(str) + "_" + df['winner'] + "_" + df['loser']

# Identificar qué equipo pateó primero en todo el partido
first_kicking_teams = df[df['first_taker'] == True][['match_id', 'team']].drop_duplicates()
first_kicking_teams['kicked_first'] = True

# Unir esta etiqueta al dataset principal
df = df.merge(first_kicking_teams, on=['match_id', 'team'], how='left')
df['kicked_first'] = df['kicked_first'].fillna(False)

# Prepare data for the Tornado Chart
# Filtrar solo los primeros 5 penales reglamentarios
df_filtered = df[df['penalty_order'] <= 5]

# Calcular conversión por ronda y por orden de pateo
conversion_rates = df_filtered.groupby(['penalty_order', 'kicked_first'])['scored'].mean().reset_index()
conversion_rates['conversion_pct'] = (conversion_rates['scored'] * 100).round(1)

team1_data = conversion_rates[conversion_rates['kicked_first'] == True].sort_values('penalty_order')
team2_data = conversion_rates[conversion_rates['kicked_first'] == False].sort_values('penalty_order')

# 4. Crear el Gráfico Tornado en Plotly
y_labels = [f"Round {i}" for i in range(1, 6)]
fig_tornado = go.Figure()

# Barras: Patea 1º (Valores negativos para que crezcan hacia la izquierda)
fig_tornado.add_trace(go.Bar(
    y=y_labels,
    x=-team1_data['conversion_pct'],
    name='Shooted First',
    orientation='h',
    marker_color='#86efac',
    text=team1_data['conversion_pct'].astype(str) + '%',
    textposition='inside',
    hoverinfo='text',
    hovertext='Round ' + team1_data['penalty_order'].astype(str) + '<br>Conversion: ' + team1_data['conversion_pct'].astype(str) + '%'
))

# Barras: Patea 2º (Valores positivos para que crezcan hacia la derecha)
fig_tornado.add_trace(go.Bar(
    y=y_labels,
    x=team2_data['conversion_pct'],
    name='Shooted Second',
    orientation='h',
    marker_color='#fca5a5',
    text=team2_data['conversion_pct'].astype(str) + '%',
    textposition='inside',
    hoverinfo='text',
    hovertext='Round ' + team2_data['penalty_order'].astype(str) + '<br>Conversion: ' + team2_data['conversion_pct'].astype(str) + '%'
))

# Truco de diseño: Ajustar los ejes para que los números negativos se vean como positivos
fig_tornado.update_layout(
    barmode='overlay', height=400,
    xaxis=dict(
        tickvals=[-100, -75, -50, -25, 0, 25, 50, 75, 100],
        ticktext=['100%', '75%', '50%', '25%', '0', '25%', '50%', '75%', '100%'],
        range=[-110, 110], title='Conversion Rate (%)'
    ),
    yaxis=dict(autorange="reversed"), margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
)
fig_tornado = style_plotly(fig_tornado, height=400, margin=dict(l=0, r=0, t=30, b=0))
render_plot(fig_tornado)

# Macro Conclusion
st.success("💡 **Insight:** The team kicking second suffers a drastic drop in effectiveness between Rounds 2 and 4. The rebound in Round 5 is explained by 'Survivorship Bias': only specialists in very tight shootouts get to take the last penalty.")

render_divider()



# MICRO CHARTS (Two in the same row)
render_section("Impact and Risk Analysis")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    # Bar: scoring first penalty gives higher chance to win 
    first_scored_win = df_penalty[(df_penalty["penalty_order"]==1) & (df_penalty["scored"]==True) & (df_penalty["winner"]==df_penalty["team"])].shape[0]
    first_missed_win = df_penalty[(df_penalty["penalty_order"]==1) & (df_penalty["scored"]==False) & (df_penalty["winner"]==df_penalty["team"])].shape[0]
    first_scored_total = df_penalty[(df_penalty["penalty_order"]==1) & (df_penalty["scored"]==True)].shape[0]
    first_missed_total = df_penalty[(df_penalty["penalty_order"]==1) & (df_penalty["scored"]==False)].shape[0]

    first_scored_win_rate = first_scored_win / first_scored_total * 100
    first_missed_win_rate = first_missed_win / first_missed_total * 100

    df_chart = pd.DataFrame({
        "First penalty": [
            "Scored",
            "Missed",
        ],
        "Win rate": [
            first_scored_win / first_scored_total * 100,
            first_missed_win / first_missed_total * 100,
        ],
    })

    fig = px.bar(
        df_chart,
        x="First penalty",
        y="Win rate",
        text="Win rate",
        labels={"First penalty": "First penalty outcome", "Win rate": "Win rate (%)"},
    )

    fig.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="outside",
    )

    fig.update_yaxes(
        title="Win rate (%)",
        range=[0, 100],
    )

    fig.update_layout(
        showlegend=False,
    )
    fig = style_plotly(fig)

    render_section("The 'First Blood' Impact: Win Rate if 1st Penalty is Scored", "The real advantage comes from scoring first, not from winning the coin toss.")
    render_plot(fig, theme="streamlit")
    st.caption("The real advantage isn't winning the coin toss, it's scoring first.")


with col_graf2:
    render_section("Shootout Duration: Reaching the 5th Kick", "The risk of saving your best player.")
    # 5th Kick Bar
    max_penalty = (
        df_penalty.groupby(["year", "round", "winner", "loser"])
        .agg(
            max_penalty=("penalty_order", "max")
        )
        .reset_index()
    )

    ended_before = max_penalty[max_penalty["max_penalty"]<5].shape[0]
    reached_fifth = max_penalty[max_penalty["max_penalty"]==5].shape[0]
    total = ended_before + reached_fifth

    df_chart = pd.DataFrame({
        "Category": [
            "Ended before 5th kick",
            "Reached 5th kick",
        ],
        "Count": [
            ended_before,
            reached_fifth,
        ]
    })

    df_chart["Percentage"] = df_chart["Count"] / total * 100

    fig = px.bar(
        df_chart,
        x="Percentage",
        y=["Shootouts"] * len(df_chart),   # una sola barra
        color="Category",
        orientation="h",
        text=df_chart["Percentage"].round(1).astype(str) + "%",
        labels={"Percentage": "Share of shootouts (%)", "Shootouts": "Shootouts"},
        custom_data=["Category"],
    )

    fig.update_traces(
        textposition="inside",
        hovertemplate=(
            "Category: %{customdata[0]}<br>"
            "Share of Shootouts: %{x:.1f}%"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        barmode="stack",
        showlegend=True,
        xaxis_title="Percentage of shootouts",
        yaxis_title="",
    )

    fig.update_xaxes(range=[0, 100])
    fig = style_plotly(fig)

    render_plot(fig, theme="streamlit")
    st.caption("A high percentage of shootouts end earlier. Saving the 'specialist' can be fatal.")

st.success("💡 **Insight:** Early moments matter most. Teams that score the opening penalty win far more often, while nearly one-third of shootouts end before the fifth kick is even taken.")

render_data_source()