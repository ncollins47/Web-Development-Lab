# This creates the page for users to input data.
# The collected data is appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os  # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="🎻",
)

# COLUMN NAMES (must match the header row in data.csv exactly)
COLUMNS = ["nickname", "favorite_album", "listening_spot", "mood", "vibe_word", "hours_per_week"]

# ANSWER CHOICES
ALBUMS = [
    "Typical of Me",
    "Everything I Know About Love",
    "Bewitched",
    "A Night at the Symphony",
    "A Night at the Symphony: Live at the Hollywood Bowl",
    "A Matter of Time",
    "A Very Laufey Holiday: The Santa Claus Is Comin' To Town Edition",
]
SPOTS = ["Rainy window", "Late-night drive", "Studying", "Cooking", "Walking to class", "Falling asleep"]
MOODS = ["Dreamy", "Nostalgic", "Romantic", "Cozy", "Melancholy", "Hopeful"]

# A little blurb shown after submitting, based on the mood they picked
BLURBS = {
    "Dreamy": "You live in a soft-focus, slow-dance kind of world. 🌙",
    "Nostalgic": "You miss moments you haven't even finished living yet. 📼",
    "Romantic": "Candlelight, a piano, and absolutely no notes on your phone. 🕯️",
    "Cozy": "Blanket, tea, rain on the window. You've already won. ☕",
    "Melancholy": "Beautifully sad is your love language. 🥀",
    "Hopeful": "You hear a bossa nova and assume things are turning around. ☀️",
}

# PAGE TITLE AND USER DIRECTIONS (with a custom gradient header)
st.markdown(
    """
    <style>
    .survey-hero {
        background: linear-gradient(135deg, #f6e7d8 0%, #f4b6b6 55%, #9cc7f5 100%);
        border-radius: 22px; padding: 28px 32px; margin-bottom: 18px;
    }
    .survey-hero h1 { color:#1b2a41; font-family: Georgia, serif; margin:0; padding:0; }
    .survey-hero p  { color:#3b4a63; font-style: italic; margin:6px 0 0 0; }
    </style>
    <div class="survey-hero">
      <h1>The Laufey Listener Survey 🎻</h1>
      <p>Tell us how you listen. Your answers get added to the charts on the Visuals page.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# DATA INPUT FORM
with st.form("survey_form", clear_on_submit=True):
    nickname = st.text_input("What should we call you?", placeholder="e.g. Jazzy Jo")
    favorite_album = st.selectbox("Which album do you play the most?", ALBUMS)
    listening_spot = st.selectbox("Where do you usually listen?", SPOTS)
    mood = st.radio("Pick the mood that fits her music best:", MOODS, horizontal=True)
    vibe_word = st.text_input("Describe Laufey's music in ONE word:", placeholder="velvet")
    hours_per_week = st.slider("About how many hours a week do you listen?", 0, 40, 5)

    # The submit button for the form.
    submitted = st.form_submit_button("Add my answers 🎶")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        if not nickname.strip() or not vibe_word.strip():
            st.warning("Please fill in your nickname and your one-word vibe first.")
        else:
            # 1. Create a new row of data from the inputs.
            new_row = pd.DataFrame(
                [
                    {
                        "nickname": nickname.strip(),
                        "favorite_album": favorite_album,
                        "listening_spot": listening_spot,
                        "mood": mood,
                        "vibe_word": vibe_word.strip().lower(),
                        "hours_per_week": hours_per_week,
                    }
                ],
                columns=COLUMNS,
            )

            # 2. Append it to data.csv in 'append' mode.
            #    Only write the header if the file is missing or empty.
            write_header = not os.path.exists("data.csv") or os.path.getsize("data.csv") == 0
            new_row.to_csv("data.csv", mode="a", header=write_header, index=False)

            st.success(f"Your data has been submitted! Thanks, {nickname.strip()}. {BLURBS[mood]}")
            st.balloons()


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider()  # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    current_data_df = pd.read_csv("data.csv")
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
