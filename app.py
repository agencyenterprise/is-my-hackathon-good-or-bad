import os
import random
from textwrap import dedent

import openai
import streamlit as st

TOPICS = [
    "chickens",
    "dogs",
    "cats",
    "birds",
    "mice",
    "snakes",
    "turtles",
    "hamsters",
    "pigs",
    "sheep",
    "goats",
    "dolphins",
    "penguins",
    "polar bears",
    "monsters",
    "zombies",
    "ghosts",
    "vampires",
    "werewolves",
    "politicians",
    "scientists",
    "astronauts",
    "astronomers",
    "phd students",
    "pilots",
    "physicians",
    "physicists"
]


@st.cache
def generate_parody(lyrics, topic):
    prompt = f"Modify the lyrics to be about {topic}:\n----\n{lyrics}\n----",
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.8,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["----"]
    )
    return response["choices"][0]["text"]


@st.cache
def get_items(city):
    response = openai.Completion.create(
        engine="curie",
        prompt=f"For a trip to {city}, you should bring:\n*",
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.2,
    )
    return response["choices"][0]["text"].splitlines()


@st.cache
def load_lyrics():
    with open("lyrics.txt", "r", newline='') as f:
        lyrics = f.read().split('----\n')
    return lyrics


def main():
    st.header("🎶 Parodies Generator")
    description_text = dedent("""
    Add the lyrics below and choose a topic to create a parody.
    We will modify the lyrics to make it about the chosen topic.
    """)
    st.write(description_text)
    default_lyrics = load_lyrics()

    topic_input = st.empty()
    lyrics_input = st.empty()
    lyrics = lyrics_input.text_area(
        "Lyrics")
    selected_topic = selected_topic = topic_input.text_input(
        "Topic")

    randomize_button = st.button("Generate random parody!")
    generate_button = st.button("Generate parody!")

    if randomize_button:
        lyrics = lyrics_input.text_area(
            "Lyrics", random.choice(default_lyrics))
        selected_topic = selected_topic = topic_input.text_input(
            "Topic", random.choice(TOPICS))
        try:
            parody = generate_parody(lyrics, selected_topic)
        except:
            st.text(f"Something went wrong. Please try again.")
        else:
            st.text(parody)

    if generate_button:
        try:
            parody = generate_parody(lyrics, selected_topic)
        except:
            st.text(f"Something went wrong. Please try again.")
        else:
            st.text(parody)


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()
