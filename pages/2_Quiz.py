import streamlit as st
from streamlit_image_select import image_select



st.title("✨ Glitter ✨ or 💥 Bitter 💥")
st.subheader("Take this quiz to find the pony that matches your power of friendship!")

scoreR=0

st.text("By taking this test you agree to the powers of magic and happiness being used to determine your character")
st.checkbox("I agree")
st.divider()

#QUESTION ONE
genre = st.radio(
    "What type of movie are you putting on to reset your sparkle?",
    [":rainbow[Comedy]", "***Drama***", "Documentary 📷 ", ":blue[Action]"]) #NEW

if genre == ":rainbow[Comedy]":
    st.write("You selected comedy.")
    scoreR += 2
elif genre == "***Drama***":
    st.write("You selected drama.")
    scoreR += 3
elif genre == "Documentary 📷 ":
    st.write("You selected documentary.")
    scoreR += 1
else:
    st.write("You selected action.")
    scoreR += 4

st.divider()

#QUESTION TWO
hobby = st.radio("When your not out helping people with friendship, what are you up to?",
                 ["📚Reading", "🏃Working Out","🍰Baking","👗Playing Dress Up"])

if hobby == "📚Reading":
    st.image("Images/reading.jpg",width = 300)
    scoreR += 1
elif hobby == "🏃Working Out":
    st.image("Images/workout.jpg",width = 300)
    scoreR += 4
elif hobby == "🍰Baking":
    st.image("Images/baking.jpg",width = 300)
    scoreR += 2
else:
    st.image("Images/dressup.jpg",width = 300)
    scoreR += 3

st.divider()

#QUESTION THREE
    
ponymark = st.selectbox(
    "What is your dream Ponymark?",
    ("Butterflies", "Balloons", "Sparkles", "A Rainbow"),
    index=None,
    placeholder="Select...",
) #NEW

st.write("You selected:", ponymark)

if ponymark=="Butterflies":
    scoreR += 1
elif ponymark=="Balloons":
    scoreR += 2
elif ponymark=="Sparkles":
    scoreR += 3
else:
    ponymark=="A Rainbow"
    scoreR += 4
st.divider()

#QUESTION FOUR
favColor = st.select_slider(
"Select a color of the rainbow",
options=[ ":red[red]", ":orange[orange]", ":yellow[yellow]",":green[green]",":blue[blue]",":violet[violet]"])
st.write("My favorite color is", favColor) #NEW

if favColor == [":red[red]", ":orange[orange]", ":yellow[yellow]"]:
    scoreR += 2
else:
    scoreR+= 4

st.divider()

#QUESTION FIVE
options=["Spike","Princess Luna","Sunset Shimmer","Apple Bloom"] #NEW
choice = image_select("Who would you want as your partner-in-crime?",
                        images=["Images/spike.jpg",
                                "Images/luna.jpg",
                                "Images/sunset.jpg",
                                "Images/bloom.jpg"],
                        captions=options,
                        return_value="index",)

sideKick=options[choice]
if sideKick=="Spike":
    scoreR += 1
elif sideKick=="Princess Luna":
    scoreR += 3
elif sideKick == "Sunset Shimmer":
    scoreR += 4
else:
    scoreR += 2

st.divider()

#RESULTS

if st.button("Find my pony!"):
    if scoreR <= 9:
        pony = "Twilight Sparkle"
        message = "Smart, organized, and always up for a book."
        pic = "Images/twilight.jpg"
    elif scoreR <= 12:
        pony = "Fluttershy"
        message = "Gentle, kind, and a friend to every animal."
        pic = "Images/fluttershy.jpg"
    elif scoreR <= 16:
        pony = "Rarity"
        message = "Generous, stylish, and a little dramatic."
        pic = "Images/rarity.jpg"
    else:
        pony = "Rainbow Dash"
        message = "Fast, bold, and loyal to the end."
        pic = "Images/rainbowdash.jpg"

    st.header(f"You are {pony}! 🦄")
    st.write(message)
    st.image(pic, width=300)
    st.balloons()

    
                        

    
    
    
    
