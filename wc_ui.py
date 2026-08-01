import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --wc-bg: #0a0f1d;
            --wc-bg-soft: #0f1728;
            --wc-sidebar: #111827;
            --wc-surface: rgba(19, 27, 46, 0.9);
            --wc-surface-strong: rgba(26, 37, 62, 0.96);
            --wc-text: #eef4ff;
            --wc-muted: #a9b7cc;
            --wc-border: rgba(148, 163, 184, 0.18);
            --wc-accent-strong: #7dd3fc;
            --wc-accent-warm: #f8c471;
            --wc-positive: #86efac;
            --wc-negative: #fca5a5;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(125, 211, 252, 0.12), transparent 30%),
                radial-gradient(circle at top right, rgba(248, 196, 113, 0.09), transparent 24%),
                linear-gradient(180deg, #0d1424 0%, var(--wc-bg) 52%, #070b14 100%);
            color: var(--wc-text);
        }

        header[data-testid="stHeader"] {
            background: transparent;
            height: 0;
        }

        [data-testid="stToolbar"] {
            background: transparent;
            border: none;
            box-shadow: none;
        }

        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        button[data-testid^="stBaseButton-header"],
        button[kind="header"] {
            top: 0.9rem;
            left: 0.9rem;
        }

        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"] button,
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button,
        button[data-testid^="stBaseButton-header"],
        button[kind="header"] {
            width: 2rem;
            height: 2rem;
            border-radius: 999px;
            background: transparent !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            color: var(--wc-accent-strong) !important;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        [data-testid="collapsedControl"] *,
        [data-testid="stSidebarCollapsedControl"] *,
        [data-testid="stSidebarCollapseButton"] *,
        button[data-testid^="stBaseButton-header"] *,
        button[kind="header"] * {
            color: var(--wc-accent-strong) !important;
        }

        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        button[data-testid^="stBaseButton-header"] svg,
        button[kind="header"] svg,
        [data-testid="collapsedControl"] path,
        [data-testid="stSidebarCollapsedControl"] path,
        [data-testid="stSidebarCollapseButton"] path,
        button[data-testid^="stBaseButton-header"] path,
        button[kind="header"] path {
            fill: currentColor !important;
            stroke: var(--wc-accent-strong) !important;
        }

        [data-testid="stToolbar"] button,
        [data-testid="stDeployButton"] button,
        button[data-testid^="stBaseButton-header"],
        button[kind="header"] {
            outline: none !important;
        }

        [data-testid="stToolbar"] button:hover,
        [data-testid="stToolbar"] button:focus,
        [data-testid="stToolbar"] button:focus-visible,
        [data-testid="stToolbar"] button:active,
        [data-testid="stDeployButton"] button:hover,
        [data-testid="stDeployButton"] button:focus,
        [data-testid="stDeployButton"] button:focus-visible,
        [data-testid="stDeployButton"] button:active,
        button[data-testid^="stBaseButton-header"]:hover,
        button[data-testid^="stBaseButton-header"]:focus,
        button[data-testid^="stBaseButton-header"]:focus-visible,
        button[data-testid^="stBaseButton-header"]:active,
        button[kind="header"]:hover,
        button[kind="header"]:focus,
        button[kind="header"]:focus-visible,
        button[kind="header"]:active {
            background: transparent !important;
            border-color: transparent !important;
            box-shadow: none !important;
            color: var(--wc-accent-strong) !important;
        }

        [data-testid="stToolbar"] button *,
        [data-testid="stDeployButton"] button *,
        button[data-testid^="stBaseButton-header"] *,
        button[kind="header"] * {
            background: transparent !important;
            box-shadow: none !important;
        }

        section.main > div {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #0c1220 100%);
            border-right: 1px solid var(--wc-border);
            color: var(--wc-text);
        }

        [data-testid="stSidebar"] * {
            color: var(--wc-text) !important;
        }

        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] [role="button"] {
            color: var(--wc-text) !important;
        }

        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] textarea,
        [data-baseweb="select"] > div,
        [data-baseweb="popover"] {
            background: var(--wc-surface-strong) !important;
            border-color: var(--wc-border) !important;
        }

        [data-baseweb="select"] svg,
        [data-testid="stSidebar"] svg {
            color: var(--wc-accent-strong) !important;
            fill: currentColor !important;
        }

        h1, h2, h3, h4 {
            color: var(--wc-text);
            letter-spacing: 0;
        }

        .wc-hero {
            padding: 0.35rem 0 0.6rem;
        }

        .wc-eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 0.72rem;
            color: var(--wc-accent-strong);
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .wc-title {
            font-size: clamp(2rem, 3.4vw, 3.1rem);
            font-weight: 750;
            line-height: 1.05;
            margin-bottom: 0.25rem;
        }

        .wc-subtitle {
            color: var(--wc-muted);
            font-size: 1rem;
            max-width: 62rem;
        }

        .wc-section-title {
            font-size: 1.35rem;
            font-weight: 700;
            margin: 0.1rem 0 0.1rem;
            color: var(--wc-text);
        }

        .wc-section-desc {
            color: var(--wc-muted);
            margin-bottom: 0.2rem;
        }

        .wc-divider {
            border: none;
            border-top: 1px solid var(--wc-border);
            margin: 1.45rem 0;
        }

        div[data-testid="stMetric"] {
            background: var(--wc-surface);
            border: 1px solid var(--wc-border);
            min-height: 144px;
            padding: 1rem 1rem 0.85rem;
            border-radius: 12px;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.22);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        div[data-testid="stMetric"] label {
            color: var(--wc-muted);
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: var(--wc-text);
        }

        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-size: 0.68rem;
            color: var(--wc-muted) !important;
            font-weight: 600;
            line-height: 1.1;
            margin-top: 0.15rem;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
            border: 1px solid var(--wc-border);
        }

        div[data-testid="stInfo"] {
            background: rgba(125, 211, 252, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.22);
        }

        div[data-testid="stSuccess"] {
            background: rgba(20, 83, 45, 0.46);
            border: 1px solid rgba(134, 239, 172, 0.24);
            color: var(--wc-text);
        }

        div[data-testid="stSuccess"] * {
            color: var(--wc-text) !important;
        }

        div[data-testid="stSuccess"] strong,
        div[data-testid="stSuccess"] b {
            color: var(--wc-positive) !important;
        }

        .stCaptionContainer,
        [data-testid="stCaptionContainer"],
        label,
        p {
            color: var(--wc-muted);
        }

        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text,
        .js-plotly-plot .g-gtitle,
        .js-plotly-plot .legendtext,
        .js-plotly-plot .colorbar text {
            fill: var(--wc-text) !important;
            color: var(--wc-text) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, eyebrow: str = "World Cup Analytics") -> None:
    st.markdown(
        f"""
        <div class="wc-hero">
            <div class="wc-eyebrow">{eyebrow}</div>
            <div class="wc-title">{title}</div>
            <div class="wc-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section(title: str, description: str | None = None) -> None:
    st.markdown(f'<div class="wc-section-title">{title}</div>', unsafe_allow_html=True)
    if description:
        st.markdown(f'<div class="wc-section-desc">{description}</div>', unsafe_allow_html=True)


def render_divider() -> None:
    st.markdown('<hr class="wc-divider" />', unsafe_allow_html=True)


def render_metric_row(items: list[dict[str, object]]) -> None:
    columns = st.columns(len(items))
    for column, item in zip(columns, items):
        with column:
            metric_kwargs = dict(item)
            if "delta" not in metric_kwargs:
                metric_kwargs["delta"] = " "
                metric_kwargs["delta_color"] = "off"
            st.metric(**metric_kwargs)


def style_plotly(fig, *, height: int | None = None, margin: dict | None = None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,40,0.48)",
        font=dict(family="Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif", color="#eef4ff"),
        colorway=["#7dd3fc", "#f8c471", "#86efac", "#fca5a5", "#c4b5fd", "#67e8f9", "#f9a8d4"],
        hoverlabel=dict(bgcolor="#131b2e", bordercolor="#334155", font=dict(color="#eef4ff")),
        legend=dict(font=dict(color="#eef4ff"), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(
            title_font=dict(color="#d8e3f5"),
            tickfont=dict(color="#a9b7cc"),
            gridcolor="rgba(148,163,184,0.14)",
            zerolinecolor="rgba(148,163,184,0.26)",
            linecolor="rgba(148,163,184,0.22)",
        ),
        yaxis=dict(
            title_font=dict(color="#d8e3f5"),
            tickfont=dict(color="#a9b7cc"),
            gridcolor="rgba(148,163,184,0.14)",
            zerolinecolor="rgba(148,163,184,0.26)",
            linecolor="rgba(148,163,184,0.22)",
        ),
        dragmode=False,
        margin=margin or dict(l=0, r=0, t=30, b=0),
    )
    if height is not None:
        fig.update_layout(height=height)
    return fig


def render_plot(fig, *, width: str = "stretch", height: int | None = None, theme: str | None = None):
    if theme is not None:
        kwargs = {"theme": theme}
    else:
        kwargs = {}

    fig = style_plotly(fig, height=height)
    st.plotly_chart(
        fig,
        width=width,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "doubleClick": False,
            "responsive": True,
            "showTips": False,
        },
        **kwargs,
    )

def render_data_source():
    st.divider()
    st.caption(
        "Data source: Fjelstul, Joshua C. *The Fjelstul World Cup Database* v1.2.0 (July 19, 2023). "
        "https://github.com/jfjelstul/worldcup"
    )