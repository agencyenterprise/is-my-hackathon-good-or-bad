import os

import openai
import streamlit as st


@st.cache
def get_attractions(city):
    prompt = f"Q: What are the top five tourist attractions of Paris?\nA: Eiffel Tower; Louvre Museum; Notre-Dame; Musée d'Orsay; Champs-Élysées Avenue.\n###\nQ: What are the top five tourist attractions of New York?\nA: Empire State Building; Statue of Liberty; Times Square; Central Park; Broadway\n###\nQ: What are the top five tourist attractions of London?\nA: Buckingham Palace; Big Ben; Tower Bridge; London Eye; St. Paul's Cathedral.\n###\nQ: What are the top five tourist attractions of Rome?\nA: Colosseum; Vatican; Trevi Fountain; Spanish Steps; Piazza Navona.\n###\nQ: What are the top five tourist attractions of {city}?\nA:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"],
    )
    return response["choices"][0]["text"].splitlines()[0].split(";")


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


def stripe_other_cities(items):
    """Remove repetition that GPT-3 might generate"""
    for item in items:
        if item.startswith("For a trip to"):
            return
        yield item


def main():
    selected_city = st.text_input("City", max_chars=30)

    if selected_city:
        try:
            attractions = get_attractions(selected_city)
        except:
            st.text(f"Couldn't find the city {selected_city}")
        else:
            st.subheader("Top-5 attractions")
            st.markdown("\n".join([f'* {x.rstrip(".")}' for x in attractions]))
            st.subheader("What you should bring with you")
            items = get_items(selected_city)
            items = [x.split("*") for x in items]
            items = [item for sublist in items for item in sublist if item]
            items = list(stripe_other_cities(items))
            st.markdown("\n".join([f'* {x.lstrip("-")}' for x in items]))


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()
