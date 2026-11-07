# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import plotly.express as px
from pathlib import Path


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualization: Laufey Albums Overview 💿")

with open("data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["data_points"])


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
st.header("Album Covers")

base_dir = Path(__file__).resolve().parent.parent

cols = st.columns(len(df))
for col, (_, row) in zip(cols, df.iterrows()):
    image_path = base_dir / row["image"]
    with col:
        if image_path.exists():
            st.image(str(image_path), caption=f"{row['label']} ({row['year']})", use_container_width=True)
        else:
            st.caption(f"Missing image for {row['label']}")
st.divider() 
            
st.header("Tracks per Album")

static_fig = px.bar(
    df,
    x= "label",
    y= "tracks",
    color= "label",
    title= f"{data['chart_title']}: Number of Tracks per Album",
    labels= {"label": "Album", "tracks": "Number of Tracks"},
)
st.plotly_chart(static_fig, use_container_width=True) #ADVANCED

st.divider() 
st.header("Explore Laufey's Albums Over Time")

if "metric" not in st.session_state:
    st.session_state.metric = "tracks"
if "year_range" not in st.session_state:
    st.session_state.year_range = (int(df["year"].min()), int(df["year"].max()))

st.radio(
    "Choose a metric for the y-axis:",
    options=["tracks", "minutes"],
    format_func=lambda m: "Number of Tracks" if m == "tracks" else "Runtime (minutes)",
    key="metric",
)
st.slider(
    "Year range:",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    key="year_range",
)

low, high = st.session_state.year_range
filtered = df[(df["year"] >= low) & (df["year"] <= high)]
st.divider() 
metric_label = "Number of Tracks" if st.session_state.metric == "tracks" else "Runtime (minutes)"

dynamic_fig = px.scatter(
    filtered,
    x= "year",
    y=st.session_state.metric,
    color= "label",
    hover_name= "label",
    title= f"{metric_label} by Release Year",
    labels={
        "year": "Release Year",
        st.session_state.metric: metric_label,
        "label": "Album",
    },
)
dynamic_fig.update_traces(marker=dict(size=16))
dynamic_fig.update_xaxes(dtick=1)
st.plotly_chart(dynamic_fig, use_container_width=True)



# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.divider()
st.header("🎤 Listener Survey Results")
st.caption("Live data from the Survey page (data.csv).")

try:
    survey_df = pd.read_csv("data.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    survey_df = pd.DataFrame()

if survey_df.empty:
    st.info("No survey responses yet. Head to the Survey page and add some!")
else:
    #fun metric cards
    top_album = survey_df["favorite_album"].mode()[0]
    top_word = survey_df["vibe_word"].mode()[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Listeners surveyed", len(survey_df))
    c2.metric("Avg hours / week", f"{survey_df['hours_per_week'].mean():.1f}")
    c3.metric("Most-used vibe word", f'"{top_word}"')

    # shared Laufey-inspired palettes (the dynamic chart cycles through them)
    PALETTES = {
        "Cream & Rose": ["#F6E7D8", "#F4B6B6", "#E58F9B", "#B5657A", "#7A3E5C", "#3F2145", "#C9A7C7"],
        "Hollywood Bowl": ["#F8D49A", "#EE8C5B", "#D2493F", "#8E2F4B", "#52305F", "#2E2A5C", "#7B8FD1"],
        "Matter of Time": ["#C7E8F3", "#8CC5E3", "#4F9DB5", "#2E7A8C", "#255D70", "#1B3F57", "#9AD0C2"],
    }
    palette_names = list(PALETTES)

   
    st.subheader("Which album do listeners play the most?")
    album_counts = survey_df["favorite_album"].value_counts().reset_index()
    album_counts.columns = ["Album", "Listeners"]

    donut = px.pie(
        album_counts,
        names="Album",
        values="Listeners",
        hole=0.55,
        color_discrete_sequence=PALETTES["Cream & Rose"],
        title="Listeners' Most-Played Laufey Album",
    )
    donut.update_traces(textinfo="percent", textfont_size=15, marker=dict(line=dict(color="#0e1117", width=3)))
    donut.update_layout(
        legend_title_text="Album",
        annotations=[dict(text="🎻<br>favorites", x=0.5, y=0.5, font_size=18, showarrow=False)],
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f6e7d8"),
    )
    st.plotly_chart(donut, use_container_width=True)

    st.divider()


    st.subheader("How long do different listeners listen?")

    # session state: remembers which palette is active between clicks
    if "palette_idx" not in st.session_state:
        st.session_state.palette_idx = 0
    if "palette_clicks" not in st.session_state:
        st.session_state.palette_clicks = 0

    def next_palette():
        st.session_state.palette_idx = (st.session_state.palette_idx + 1) % len(palette_names)
        st.session_state.palette_clicks += 1

    group_options = {
        "Mood": "mood",
        "Listening spot": "listening_spot",
        "Favorite album": "favorite_album",
    }
    choice = st.radio("Group listeners by:", list(group_options), horizontal=True, key="group_choice")
    st.button("🎨 Change palette", on_click=next_palette)

    col = group_options[choice]
    grouped = (
        survey_df.groupby(col)
        .agg(avg_hours=("hours_per_week", "mean"), listeners=("nickname", "count"))
        .reset_index()
        .sort_values("avg_hours")
    )
    grouped["avg_hours"] = grouped["avg_hours"].round(1)

    active = palette_names[st.session_state.palette_idx]
    bars = px.bar(
        grouped,
        x="avg_hours",
        y=col,
        orientation="h",
        color=col,
        text="avg_hours",
        hover_data={"listeners": True},
        color_discrete_sequence=PALETTES[active],
        title=f"Average Weekly Listening Hours by {choice}",
        labels={"avg_hours": "Average Hours per Week", col: choice, "listeners": "Listeners"},
    )
    bars.update_traces(textposition="outside", marker_line_color="#0e1117", marker_line_width=2)
    bars.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f6e7d8"),
        xaxis=dict(gridcolor="rgba(246,231,216,0.15)"),
    )
    st.plotly_chart(bars, use_container_width=True)
    st.caption(f"Palette: **{active}** · changed {st.session_state.palette_clicks} time(s) this session")

    with st.expander("🔍 See the raw survey responses"):
        st.dataframe(survey_df, use_container_width=True)
